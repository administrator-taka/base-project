import datetime
import datetime
import logging
import time
from datetime import datetime
from typing import List

from django.db.models import Prefetch

from myapp.applications.domain.logic.youtube_api_logic import YouTubeApiLogic
from myapp.applications.domain.logic.youtube_subtitle_logic import YouTubeSubtitleLogic
from myapp.applications.util.code.subtitle_status import SubtitleStatus
from myapp.applications.util.code.subtitle_type import SubtitleType
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myapp.applications.util.file_handler import FileHandler
from myapp.applications.util.util_generate import generate_subtitle_id, generate_uuid
from myapp.models import VideoSubtitleInfo, VideoSubtitle, SubtitleTranslation, ChannelDetail, VideoDetail, \
    ChannelTranslationInfo, SubtitleLearningMemory
from myproject.settings.base import TEST_DIR


class VideoService:
    def __init__(self):
        self.youtube_subtitle_logic = YouTubeSubtitleLogic()
        self.youtube_api_logic = YouTubeApiLogic()

    def get_video_data(self, video_id):
        video_detail_dict = {}
        try:
            video_detail = VideoDetail.objects.get(video_id=video_id)
            channel_translation_info = ChannelTranslationInfo.objects.filter(channel_id=video_detail.channel_id).first()
            if video_detail.initial_flag:
                video_detail_dict = {
                    'title': video_detail.title,
                    'description': video_detail.description,
                    'video_id': video_detail.video_id,
                    'published_at': video_detail.published_at,
                    'channel_id': video_detail.channel_id.channel_id,
                    'default_language': video_detail.default_language,
                    'default_video_audio_language': video_detail.default_audio_language,
                    'actual_start_time': video_detail.actual_start_time,
                    'actual_end_time': video_detail.actual_end_time,
                    'scheduled_start_time': video_detail.scheduled_start_time,
                    'thumbnail': video_detail.thumbnail,
                    'default_audio_language': channel_translation_info.default_audio_language if channel_translation_info else None,
                    'translation_languages': channel_translation_info.translation_languages if channel_translation_info else None,
                }
                logging.debug("動画最新")
            else:
                video_data = self.youtube_api_logic.get_video_details_data(video_id)
                self.insert_video_data(video_data)
                video_detail_dict = {
                    'title': video_detail.title,
                    'description': video_detail.description,
                    'video_id': video_detail.video_id,
                    'published_at': video_detail.published_at,
                    'channel_id': video_detail.channel_id.channel_id,
                    'default_language': video_detail.default_language,
                    'default_video_audio_language': video_detail.default_audio_language,
                    'actual_start_time': video_detail.actual_start_time,
                    'actual_end_time': video_detail.actual_end_time,
                    'scheduled_start_time': video_detail.scheduled_start_time,
                    'thumbnail': video_detail.thumbnail,
                    'default_audio_language': channel_translation_info.default_audio_language if channel_translation_info else None,
                    'translation_languages': channel_translation_info.translation_languages if channel_translation_info else None,
                }
                logging.debug("動画更新")
        except VideoDetail.DoesNotExist:
            video_data = self.youtube_api_logic.get_video_details_data(video_id)
            if video_data:
                video_detail_dict = {
                    'title': video_data['title'],
                    'description': video_data['description'],
                    'video_id': video_data['video_id'],
                    'published_at': video_data['published_at'],
                    'channel_id': video_data['channel_id'],
                    'default_language': video_data['default_language'],
                    'default_video_audio_language': video_data['default_audio_language'],
                    'actual_start_time': video_data['actual_start_time'],
                    'actual_end_time': video_data['actual_end_time'],
                    'scheduled_start_time': video_data['scheduled_start_time'],
                    'thumbnail': video_data['thumbnail'],
                    'default_audio_language': None,
                    'translation_languages': None,
                }
            logging.debug("動画なし")

        return video_detail_dict

    # 初期字幕翻訳情報追加
    def insert_initial_subtitle_detail(self, video_id):
        try:
            video_detail = VideoDetail.objects.get(video_id=video_id)
        except VideoDetail.DoesNotExist:
            return

        default_audio_language, translation_languages = self.get_translation_info(video_detail.channel_id)
        self.update_video_caption(video_id, default_audio_language, translation_languages)

        # ベース字幕を取得
        base_subtitles = VideoSubtitle.objects.filter(
            subtitle_id__subtitle_type=SubtitleType.MANUAL.value,
            subtitle_id__video_id=video_id,
            subtitle_id__language_code=default_audio_language.value
        )

        # 各言語のターゲット字幕について翻訳を挿入
        for language in translation_languages:
            # 値が既に存在する場合はreturn
            if SubtitleTranslation.objects.filter(
                    subtitle_text_id__subtitle_id__video_id=video_id,
                    language_code=language.value
            ).exists():
                logging.debug(f"字幕解説登録済み")
                # TODO:修正前の字幕解説を更新するために毎度生成するようにしている
                # return

            # 各言語のターゲット字幕を取得
            target_subtitles = VideoSubtitle.objects.filter(
                subtitle_id__subtitle_type=SubtitleType.MANUAL.value,
                subtitle_id__video_id=video_id,
                subtitle_id__language_code=language.value
            )

            # ログ出力用
            total_subtitles = len(base_subtitles)
            processed_subtitles = 0

            if total_subtitles > 1000:
                logging.debug(f"字幕行数が多すぎます。字幕数：{total_subtitles}")
                return

            # ターゲット字幕とベース字幕をマージしてペアを見つける
            for base_subtitle in base_subtitles:
                # まず、同じ開始時間のターゲット字幕を探す
                target_subtitle = target_subtitles.filter(t_start_ms=base_subtitle.t_start_ms).first()

                # 同じ開始時間のターゲット字幕がない場合
                if not target_subtitle:
                    # ベース字幕の開始時間に最も近いターゲット字幕を見つける
                    # 前後の字幕を探す
                    previous_subtitle = target_subtitles.filter(t_start_ms__lt=base_subtitle.t_start_ms).order_by(
                        '-t_start_ms').first()
                    next_subtitle = target_subtitles.filter(t_start_ms__gt=base_subtitle.t_start_ms).order_by(
                        't_start_ms').first()

                    if previous_subtitle and next_subtitle:
                        # 前後の字幕の中でベース字幕に最も近いものを選択
                        if base_subtitle.t_start_ms - previous_subtitle.t_start_ms <= next_subtitle.t_start_ms - base_subtitle.t_start_ms:
                            target_subtitle = previous_subtitle
                        else:
                            target_subtitle = next_subtitle
                    elif previous_subtitle:
                        target_subtitle = previous_subtitle
                    elif next_subtitle:
                        target_subtitle = next_subtitle

                if target_subtitle:
                    logging.debug(f"{target_subtitle.subtitle_text}:登録中")
                    # 翻訳を挿入
                    subtitle_translation, created = SubtitleTranslation.objects.get_or_create(
                        subtitle_text_id=base_subtitle,
                        language_code=language.value,
                        defaults={
                            'subtitle_translation_text': target_subtitle.subtitle_text,
                            'subtitle_literal_translation_text': None,
                            'subtitle_translation_text_detail': None
                        }
                    )
                # 処理された字幕数を更新
                processed_subtitles += 1
                # 経過率をデバッグに出力
                logging.info(f"処理進行状況: {processed_subtitles}/{total_subtitles}")

    def get_video_subtitle_data(self, video_id):
        try:
            video_detail = VideoDetail.objects.get(video_id=video_id)
        except VideoDetail.DoesNotExist:
            return
        default_audio_language, translation_languages = self.get_translation_info(video_detail.channel_id)

        # VideoSubtitleをベースにクエリを構築
        queryset = VideoSubtitle.objects.filter(
            subtitle_id__subtitle_type=SubtitleType.MANUAL.value,
            subtitle_id__language_code=default_audio_language.value,
            subtitle_id__video_id=video_id
        ).select_related('subtitle_id').order_by('t_start_ms')

        # PrefetchでSubtitleTranslationとSubtitleLearningMemoryを取得
        queryset = queryset.prefetch_related(
            Prefetch('subtitletranslation_set',
                     queryset=SubtitleTranslation.objects.all().prefetch_related(
                         Prefetch('subtitlelearningmemory_set', queryset=SubtitleLearningMemory.objects.all())
                     ))
        )
        # 辞書のリストを初期化
        video_subtitle_data = []

        # クエリセットを実行して結果を辞書に変換
        for subtitle in queryset:
            base_subtitle_dict = {
                'subtitle_id': subtitle.subtitle_id.subtitle_id,
                'language_code': subtitle.subtitle_id.language_code,
                'subtitle_text_id': subtitle.subtitle_text_id,
                't_start_ms': subtitle.t_start_ms,
                'subtitle_text': subtitle.subtitle_text,
                'translations': []  # 翻訳の辞書
            }

            # 翻訳データを取得して辞書に追加
            for translation in subtitle.subtitletranslation_set.all():
                translation_dict = {
                    'language_code': translation.language_code,
                    'subtitle_translation_text': translation.subtitle_translation_text,
                    'subtitle_literal_translation_text': translation.subtitle_literal_translation_text,
                    'subtitle_translation_text_detail': translation.subtitle_translation_text_detail,
                    'learning_status': None  # 学習ステータスのデフォルト値
                }

                # SubtitleLearningMemoryから学習ステータスを取得
                for memory in translation.subtitlelearningmemory_set.all():
                    translation_dict['learning_status'] = memory.learning_status

                base_subtitle_dict['translations'].append(translation_dict)

            # ベース字幕と翻訳の辞書をリストに追加
            video_subtitle_data.append(base_subtitle_dict)

        return video_subtitle_data

    def single_download_video_subtitle(self, video_id):
        video_detail = VideoDetail.objects.get(video_id=video_id)
        default_audio_language, translation_languages = self.get_translation_info(video_detail.channel_id)
        self.download_video_subtitle(video_id, default_audio_language, translation_languages)

    def get_translation_info(self, channel_id):
        # ChannelTranslationInfoからデータを取得
        translation_info = ChannelTranslationInfo.objects.get(channel_id=channel_id)

        if translation_info.default_audio_language is None or translation_info.translation_languages is None:
            logging.error("TODO:デフォルト言語指定エラー")
            return
        # デフォルトの言語コードを取得
        default_audio_language = YouTubeLanguage(translation_info.default_audio_language)

        # 翻訳言語リスト取得
        translation_languages = [YouTubeLanguage(language) for language in translation_info.translation_languages]

        return default_audio_language, translation_languages

    def update_video_caption(self, video_id, default_audio_language, translation_languages):
        video_captions = self.youtube_api_logic.get_subtitle_info(video_id, default_audio_language,
                                                                  translation_languages)
        for video_caption in video_captions:
            self.insert_or_update_video_subtitle_info(video_id,
                                                      video_caption.get('subtitle_type'),
                                                      video_caption.get('language'),
                                                      SubtitleStatus.UNREGISTERED,
                                                      video_caption.get('last_updated'))

        # 自動字幕の情報追加
        self.insert_false_subtitle_info(video_id, SubtitleType.AUTOMATIC, default_audio_language)
        self.insert_false_subtitle_info(video_id, SubtitleType.MANUAL, default_audio_language)
        # 手動字幕の情報追加
        for language in translation_languages:
            self.insert_false_subtitle_info(video_id, SubtitleType.MANUAL, language)

    def insert_false_subtitle_info(self, video_id, subtitle_type, language):
        video_detail_instance, _ = VideoDetail.objects.get_or_create(video_id=video_id)
        subtitle_id = generate_subtitle_id(video_id, subtitle_type, language)
        # 既存のレコードがあれば取得
        video_subtitle_info = VideoSubtitleInfo.objects.filter(subtitle_id=subtitle_id).first()

        # 既存のレコードがある場合かつsubtitle_statusが1の場合は更新しない
        if not video_subtitle_info:
            # 既存のレコードがない場合またはsubtitle_statusが1（登録済み）でない場合は新規作成または更新
            VideoSubtitleInfo.objects.update_or_create(
                subtitle_id=subtitle_id,
                defaults={
                    'video_id': video_detail_instance,
                    'subtitle_type': subtitle_type.value,
                    'language_code': language.value,
                    'subtitle_status': SubtitleStatus.NO_SUBTITLE.value,
                    'last_updated': datetime.now(),
                    'remarks': None
                }
            )

    def insert_or_update_video_subtitle_info(self, video_id, subtitle_type, language, subtitle_status, last_updated):
        video_detail_instance, _ = VideoDetail.objects.get_or_create(video_id=video_id)
        subtitle_id = generate_subtitle_id(video_id, subtitle_type, language)

        # 既存のレコードがあれば取得
        video_subtitle_info = VideoSubtitleInfo.objects.filter(subtitle_id=subtitle_id).first()

        # 既存のレコードがある場合かつsubtitle_statusが1の場合は更新しない
        if video_subtitle_info and video_subtitle_info.subtitle_status == SubtitleStatus.REGISTERED.value:
            logging.debug("字幕登録済み")
        else:
            # 既存のレコードがない場合またはsubtitle_statusが1（登録済み）でない場合は新規作成または更新
            VideoSubtitleInfo.objects.update_or_create(
                subtitle_id=subtitle_id,
                defaults={
                    'video_id': video_detail_instance,
                    'subtitle_type': subtitle_type.value,
                    'language_code': language.value,
                    'subtitle_status': subtitle_status.value,
                    'last_updated': datetime.now(),
                }
            )

    def insert_video_data(self, video_data):
        video_id = video_data['video_id']
        e_tag = video_data['e_tag']
        title = video_data['title']
        published_at = video_data['published_at']
        description = video_data['description']
        thumbnail = video_data['thumbnail']
        channel_id = video_data['channel_id']
        default_language = video_data['default_language']
        default_audio_language = video_data['default_audio_language']
        actual_start_time = video_data['actual_start_time']
        actual_end_time = video_data['actual_end_time']
        scheduled_start_time = video_data['scheduled_start_time']
        # video_idで既存のレコードを取得する
        try:
            video_detail = VideoDetail.objects.get(video_id=video_id)
        except VideoDetail.DoesNotExist:
            # 既存のレコードがない場合は新規作成
            VideoDetail.objects.create(
                video_id=video_id,
                e_tag=e_tag,
                title=title,
                description=description,
                published_at=published_at,
                thumbnail=thumbnail,
                default_language=default_language,
                default_audio_language=default_audio_language,
                actual_start_time=actual_start_time,
                actual_end_time=actual_end_time,
                scheduled_start_time=scheduled_start_time,
                initial_flag=True,
                channel_id=ChannelDetail.objects.get(channel_id=channel_id),
            )
            logging.debug("動画情報が追加されました。")
            return

        # 既存のレコードがある場合、かつetagが異なる場合またはinitial_flagがFalseの場合にのみ更新
        if video_detail.e_tag != e_tag or not video_detail.initial_flag:
            video_detail.e_tag = e_tag
            video_detail.title = title
            video_detail.published_at = published_at
            video_detail.description = description
            if 'maxres' not in video_detail.thumbnail:
                video_detail.thumbnail = thumbnail
            video_detail.default_language = default_language
            video_detail.default_audio_language = default_audio_language
            video_detail.actual_start_time = actual_start_time
            video_detail.actual_end_time = actual_end_time
            video_detail.scheduled_start_time = scheduled_start_time
            video_detail.channel_id = ChannelDetail.objects.get(channel_id=channel_id)
            video_detail.initial_flag = True
            video_detail.save()
            logging.debug("動画情報が更新されました。")
        else:
            logging.debug("動画情報は既に最新です。")

    def download_video_subtitle(self, video_id: str,
                                default_audio_language: YouTubeLanguage,
                                translation_languages: List[YouTubeLanguage]) -> None:

        subtitle_info = self.youtube_subtitle_logic.download_subtitles_info(video_id)
        FileHandler.write_json(subtitle_info, TEST_DIR + "subtitle_data/", video_id, )
        # return
        # # TODO:データを事前に用意している場合は以下を使用
        # subtitle_info = FileHandler.get_json_response(TEST_DIR + "subtitle_data/" + video_id)
        # TODO:自動字幕は一旦取得しないようにコメントアウト（量が多すぎる）
        # 自動生成字幕
        self.create_or_update_video_subtitle_info(video_id, subtitle_info, SubtitleType.AUTOMATIC,
                                                  default_audio_language)
        # 手動作成字幕
        self.create_or_update_video_subtitle_info(video_id, subtitle_info, SubtitleType.MANUAL,
                                                  default_audio_language)

        # TODO:リストが単体だと動作不良を起こすため明示的に再度リストに格納（引数渡す時に間違ってたので多分なおっている）
        if not isinstance(translation_languages, list):
            translation_languages = [translation_languages]

        for language in translation_languages:
            self.create_or_update_video_subtitle_info(video_id, subtitle_info, SubtitleType.MANUAL,
                                                      language)

    def create_or_update_video_subtitle_info(self, video_id, subtitle_info, subtitle_type, language):
        # TODO:データを用意している場合、処理が速すぎるため念のため一時停止
        time.sleep(1)
        # 自動生成字幕
        subtitle_status, subtitle = self.youtube_subtitle_logic.extract_and_process_subtitle_json(subtitle_info,
                                                                                                  subtitle_type,
                                                                                                  language)
        # 最初にインサートし、データがあればupdateするように修正
        subtitle_id = generate_subtitle_id(video_id, subtitle_type, language)

        self.insert_or_update_video_subtitle_info(video_id,
                                                  subtitle_type,
                                                  language,
                                                  SubtitleStatus.NO_SUBTITLE,
                                                  None)
        # 字幕があった場合、
        if subtitle_status == SubtitleStatus.REGISTERED:
            self.insert_subtitle_data(video_id, subtitle, subtitle_type, language)
            VideoSubtitleInfo.objects.filter(subtitle_id=subtitle_id).update(
                subtitle_status=SubtitleStatus.REGISTERED.value,
                remarks=None
            )
        # 字幕の登録に失敗した場合
        elif subtitle_status == SubtitleStatus.REGISTRATION_FAILED:
            # サブタイトル情報がある場合、備考にサブタイトルを設定する
            VideoSubtitleInfo.objects.filter(subtitle_id=subtitle_id).update(
                subtitle_status=SubtitleStatus.REGISTRATION_FAILED.value,
                remarks=subtitle
            )

    def insert_subtitle_data(self, video_id, subtitle, subtitle_type, language):
        # 辞書型リストのデータを順番に処理してデータベースに挿入
        for data in subtitle:
            # 字幕情報を保存する前に、関連するVideoSubtitleInfoインスタンスを取得する必要があります
            subtitle_id = generate_subtitle_id(video_id, subtitle_type, language)
            subtitle_info_instance = VideoSubtitleInfo.objects.get(subtitle_id=subtitle_id)
            VideoSubtitle.objects.create(
                subtitle_id=subtitle_info_instance,
                subtitle_text_id=generate_uuid(),
                t_start_ms=data['t_start_ms'],
                d_duration_ms=data['d_duration_ms'],
                t_offset_ms=data['t_offset_ms'],
                subtitle_text=data['subtitle_text']
            )
