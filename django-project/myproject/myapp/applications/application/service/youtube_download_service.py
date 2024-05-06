import logging
import logging
import time
import unittest
from collections import defaultdict
from typing import List

from django.db.models import Q

from myapp.applications.domain.logic.youtube_api_logic import YouTubeApiLogic
from myapp.applications.domain.logic.youtube_subtitle_logic import YouTubeSubtitleLogic
from myapp.applications.util.code.subtitle_status import SubtitleStatus
from myapp.applications.util.code.subtitle_type import SubtitleType
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myapp.applications.util.file_handler import FileHandler
from myapp.applications.util.util_generate import generate_subtitle_id, generate_uuid
from myapp.models import VideoSubtitleInfo, VideoSubtitle, SubtitleTranslation, ChannelDetail, VideoDetail, \
    ChannelTranslationInfo
from myproject.settings.base import TEST_YOUTUBE_VIDEO_ID, TEST_DIR


class YoutubeDownloadService:
    def __init__(self):
        self.youtube_subtitle_logic = YouTubeSubtitleLogic()
        self.youtube_api_logic = YouTubeApiLogic()

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

    def insert_or_update_latest_subtitle_info(self, channel_id):

        default_audio_language, translation_languages = self.get_translation_info(channel_id)

        self.insert_initial_video_data(channel_id)

        playlist_videos = VideoDetail.objects.filter(channel_id=channel_id)

        # ログ出力用
        total_videos = len(playlist_videos)
        processed_videos = 0

        for video in playlist_videos:
            video_id = video.video_id
            video_captions = self.youtube_api_logic.get_subtitle_info(video_id)
            for video_caption in video_captions:
                self.insert_or_update_video_subtitle_info(video_id,
                                                          video_caption.get('subtitle_type'),
                                                          video_caption.get('language'),
                                                          SubtitleStatus.UNREGISTERED,
                                                          video_caption.get('last_updated'))

            # 自動字幕の情報追加
            self.insert_false_subtitle_info(video_id, SubtitleType.AUTOMATIC, default_audio_language)
            # 手動字幕の情報追加
            for language in translation_languages:
                self.insert_false_subtitle_info(video_id, SubtitleType.MANUAL, language)

            # 処理されたビデオ数を更新
            processed_videos += 1
            # 経過率をデバッグに出力
            logging.info(f"処理進行状況: {processed_videos}/{total_videos}")

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
                    'last_updated': last_updated,
                }
            )

    # 単語検索
    # 単語検索
    def search_single_row_word(self, search_word, channel_id=None, subtitle_type=None, language_code=None):
        # 検索クエリを構築
        query = Q(subtitle_text__icontains=search_word)

        # フィルタリング条件を追加
        if channel_id is not None:
            query &= Q(subtitle_id__video_id__channel_id=channel_id)
        if subtitle_type is not None:
            query &= Q(subtitle_id__subtitle_type=subtitle_type.value)
        if language_code is not None:
            query &= Q(subtitle_id__language_code=language_code.value)

        # VideoSubtitle モデルからレコードを検索
        results = VideoSubtitle.objects.filter(query)

        # 結果を辞書のリストに詰めて返す
        search_results = []
        for result in results:
            logging.debug(f"Video ID: {result.subtitle_id.video_id_id}")
            logging.debug(f"Start Time (ms): {result.t_start_ms}")
            logging.debug(f"Subtitle Text: {result.subtitle_text}")
            logging.debug(f"https://www.youtube.com/watch?v={result.subtitle_id.video_id_id}&t={result.t_start_ms}ms")
            result_dict = {
                "video_id": result.subtitle_id.video_id_id,
                "start_time_ms": result.t_start_ms,
                "subtitle_text": result.subtitle_text,
                "youtube_url": f"https://www.youtube.com/watch?v={result.subtitle_id.video_id_id}&t={result.t_start_ms}ms"
            }
            search_results.append(result_dict)

        return search_results

    def get_video_data(self, video_id):
        video_detail_dict = {}
        try:
            video_detail = VideoDetail.objects.get(video_id=video_id)
            if video_detail.initial_flag:
                video_detail_dict = {
                    'video_id': video_detail.video_id,
                    'title': video_detail.title,
                    'published_at': video_detail.published_at,
                    'description': video_detail.description,
                    'thumbnail': video_detail.thumbnail,
                    'channel_id': video_detail.channel_id.channel_id,
                    'default_language': video_detail.default_language,
                    'default_audio_language': video_detail.default_audio_language,
                    'actual_start_time': video_detail.actual_start_time,
                    'actual_end_time': video_detail.actual_end_time,
                    'scheduled_start_time': video_detail.scheduled_start_time
                }
                logging.debug("動画最新")
            else:
                video_data = self.youtube_api_logic.get_video_details_data(video_id)
                self.insert_video_data(video_data)
                video_detail_dict = {
                    'video_id': video_detail.video_id,
                    'title': video_detail.title,
                    'published_at': video_detail.published_at,
                    'description': video_detail.description,
                    'thumbnail': video_detail.thumbnail,
                    'channel_id': video_detail.channel_id.channel_id,
                    'default_language': video_detail.default_language,
                    'default_audio_language': video_detail.default_audio_language,
                    'actual_start_time': video_detail.actual_start_time,
                    'actual_end_time': video_detail.actual_end_time,
                    'scheduled_start_time': video_detail.scheduled_start_time
                }
                logging.debug("動画更新")
        except VideoDetail.DoesNotExist:
            video_data = self.youtube_api_logic.get_video_details_data(video_id)
            if video_data:
                video_detail_dict = {
                    'video_id': video_data['video_id'],
                    'title': video_data['title'],
                    'published_at': video_data['published_at'],
                    'description': video_data['description'],
                    'thumbnail': video_data['thumbnail'],
                    'channel_id': video_data['channel_id'],
                    'default_language': video_data['default_language'],
                    'default_audio_language': video_data['default_audio_language'],
                    'actual_start_time': video_data['actual_start_time'],
                    'actual_end_time': video_data['actual_end_time'],
                    'scheduled_start_time': video_data['scheduled_start_time']
                }
            logging.debug("動画なし")

        return video_detail_dict

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

    def get_channel_data(self, channel_id):
        self.insert_channel_data(channel_id)
        # チャンネルIDに紐づくチャンネル情報を取得
        channel_detail = ChannelDetail.objects.filter(channel_id=channel_id).first()

        # チャンネル情報を辞書型に変換して返す
        if channel_detail:
            channel_data = {
                'channel_id': channel_detail.channel_id,
                'playlist_id': channel_detail.playlist_id,
                'title': channel_detail.title,
                'description': channel_detail.description,
                'custom_url': channel_detail.custom_url,
                'published_at': channel_detail.published_at,
                'thumbnail': channel_detail.thumbnail,
                'country': channel_detail.country
            }
        else:
            # チャンネル情報が見つからない場合は空の辞書を返す
            channel_data = {}

        return channel_data

    def insert_channel_data(self, channel_id):
        # チャンネルIDに紐づくチャンネル情報を取得
        channel_data = ChannelDetail.objects.filter(
            channel_id=channel_id
        ).first()
        # チャンネル情報が存在しない場合は追加
        if not channel_data:
            channel_data = self.youtube_api_logic.get_channel_details_data(channel_id)
            if channel_data:
                # 新しいチャンネルデータを作成して保存
                new_channel = ChannelDetail.objects.create(
                    channel_id=channel_data['channel_id'],
                    playlist_id=channel_data['playlist_id'],
                    title=channel_data['title'],
                    description=channel_data['description'],
                    custom_url=channel_data['custom_url'],
                    published_at=channel_data['published_at'],
                    thumbnail=channel_data['thumbnail'],
                    country=channel_data['country']
                )
                ChannelTranslationInfo.objects.create(
                    channel_id=new_channel,
                    default_audio_language=None,
                    translation_languages=None
                )
                logging.debug("チャンネル情報が追加されました。")

            else:
                logging.debug("チャンネル情報が見つかりませんでした。")
        else:
            logging.debug("チャンネル情報は既に存在します。")

    # 初期動画データ登録
    def insert_initial_video_data(self, channel_id):
        self.insert_channel_data(channel_id)
        # チャンネルIDに紐づくチャンネル情報を取得
        channel_data = ChannelDetail.objects.filter(
            channel_id=channel_id
        ).first()
        channel_playlist_id = channel_data.playlist_id

        playlist_videos = self.youtube_api_logic.get_channel_videos(channel_playlist_id)
        for video_data in playlist_videos:
            self.insert_or_update_video_detail(video_data)

    # 動画詳細登録
    def insert_or_update_video_detail(self, video_data):
        video_id = video_data['video_id']
        e_tag = video_data['e_tag']
        title = video_data['title']
        published_at = video_data['published_at']
        description = video_data['description']
        thumbnail = video_data['thumbnail']
        channel_id = video_data['channel_id']

        # video_idで既存のレコードを取得する
        try:
            video_detail = VideoDetail.objects.get(video_id=video_id)
        except VideoDetail.DoesNotExist:
            # 既存のレコードがない場合は新規作成
            VideoDetail.objects.create(
                video_id=video_id,
                e_tag=e_tag,
                title=title,
                published_at=published_at,
                description=description,
                thumbnail=thumbnail,
                channel_id=ChannelDetail.objects.get(channel_id=channel_id),
            )
            logging.debug("動画情報が追加されました。")
            return

        # 既存のレコードがある場合、etagが異なる場合のみ更新
        if video_detail.e_tag != e_tag:
            video_detail.title = title
            video_detail.published_at = published_at
            video_detail.description = description
            video_detail.thumbnail = thumbnail
            video_detail.channel_id = ChannelDetail.objects.get(channel_id=channel_id)
            video_detail.e_tag = e_tag
            video_detail.save()
            logging.debug("動画情報が更新されました。")
        else:
            logging.debug("動画情報は既に最新です。")

    # 字幕のステータスの一覧を取得
    def get_channel_subtitle_list(self, channel_id):
        # Django ORMを使用してクエリを構築
        queryset = VideoSubtitleInfo.objects.filter(
            subtitle_type=SubtitleType.MANUAL.value,
            video_id__channel_id=channel_id
        )

        # video_idごとに字幕情報をまとめるための辞書を作成
        subtitle_info_by_video = defaultdict(list)
        for info in queryset:
            subtitle_info_by_video[info.video_id].append(info)
        # 辞書をJSON形式に変換して返す
        result = []

        # 辞書の内容を表示
        for video_detail, infos in subtitle_info_by_video.items():
            video_info = {
                'video_id': video_detail.video_id,
                'title': video_detail.title,
                'thumbnail': video_detail.thumbnail,
                'published_at': video_detail.published_at,
                'infos': [{'language_code': info.language_code, 'subtitle_status': info.subtitle_status} for info in
                          infos]
            }
            result.append(video_info)
        return result

    # 初期字幕翻訳情報追加 TODO:レスポンスを考える
    def insert_initial_subtitle_detail(self, video_id):
        # YouTubeLanguageを変数にする
        base_language = YouTubeLanguage.KOREAN
        target_language = YouTubeLanguage.JAPANESE

        # Django ORMを使用してクエリを構築
        queryset = VideoSubtitle.objects.filter(
            subtitle_id__subtitle_type=SubtitleType.MANUAL.value,
            subtitle_id__video_id=video_id
        )

        # ベース字幕のクエリ
        base_queryset = queryset.filter(subtitle_id__language_code=base_language.value)

        # ターゲット字幕のクエリ
        target_queryset = queryset.filter(subtitle_id__language_code=target_language.value)

        # クエリセットを実行
        base_results = list(base_queryset.order_by('t_start_ms'))
        target_results = list(target_queryset.order_by('t_start_ms'))

        if self.check_subtitle_text_id_exists(
                generate_subtitle_id(video_id, SubtitleType.MANUAL, base_language), target_language):
            logging.debug('既にある')
            return

        if len(base_results) == len(target_results):
            for ko_result, ja_result in zip(base_results, target_results):
                if ko_result.t_start_ms == ja_result.t_start_ms:
                    # VideoSubtitle のインスタンスを取得
                    subtitle_instance = VideoSubtitle.objects.get(subtitle_text_id=ko_result.subtitle_text_id)

                    # VideoSubtitleDetail のインスタンスを作成し、subtitle_text_id に subtitle_instance を割り当てる
                    SubtitleTranslation.objects.create(
                        subtitle_text_id=subtitle_instance,
                        language_code=target_language.value,
                        subtitle_transration_text=ja_result.subtitle_text,
                        subtitle_transration_text_detail=None,
                    )
                    print(ko_result.subtitle_text_id, ko_result.subtitle_text, ja_result.subtitle_text)
            if len(base_results)==0:
                logging.debug(f'配列サイズは一致したが一致する字幕なし。リストサイズ:{len(base_results)}')
        else:
            logging.debug('一致する字幕情報なし')

    def get_video_subtitle_data(self, video_id):
        try:
            video_detail = VideoDetail.objects.get(video_id=video_id)
        except VideoDetail.DoesNotExist:
            return 
        default_audio_language, translation_languages = self.get_translation_info(video_detail.channel_id)
        # Django ORMを使用してクエリを構築
        queryset = VideoSubtitle.objects.filter(
            subtitle_id__subtitle_type=SubtitleType.MANUAL.value,
            subtitle_id__video_id=video_id
        )

        # ベース字幕のクエリ
        base_queryset = queryset.filter(subtitle_id__language_code=default_audio_language.value)

        # ベース字幕以外のクエリ
        other_queryset = queryset.exclude(subtitle_id__language_code=default_audio_language.value)

        subtitle_translation = SubtitleTranslation.objects.filter(subtitle_text_id__in=base_queryset)

        # 辞書のリストを初期化
        video_subtitle_data = []

        # クエリセットを実行
        base_results = list(base_queryset.order_by('t_start_ms'))

        for base_result in base_results:
            base_subtitle_dict = {
                'subtitle_id': base_result.subtitle_id.subtitle_id,
                'language_code': base_result.subtitle_id.language_code,
                'subtitle_text_id': base_result.subtitle_text_id,
                't_start_ms': base_result.t_start_ms,
                'subtitle_text': base_result.subtitle_text,
                'translations': {}  # 翻訳の辞書
            }

            for language in translation_languages:
                # other_querysetのlanguage_codeで検索
                other_subtitle = other_queryset.filter(subtitle_id__language_code=language.value,
                                                       t_start_ms=base_result.t_start_ms).first()

                subtitle_translation_data = subtitle_translation.filter(
                    subtitle_text_id=base_result.subtitle_text_id,
                    language_code=language.value
                ).first()

                # 翻訳が存在する場合、辞書に追加
                if other_subtitle and subtitle_translation_data:
                    base_subtitle_dict['translations'][language.value] = {
                        'subtitle_text': other_subtitle.subtitle_text,
                        'translation_text': subtitle_translation_data.subtitle_transration_text
                    }

            # ベース字幕と翻訳の辞書をリストに追加
            video_subtitle_data.append(base_subtitle_dict)

        return video_subtitle_data

    def check_subtitle_text_id_exists(self, subtitle_id, language_code):
        # 特定の subtitle_text_id と language_code に対応する SubtitleTranslation レコードが存在するかチェック
        exists = SubtitleTranslation.objects.filter(
            subtitle_text_id__subtitle_id=subtitle_id,
            language_code=language_code.value
        ).exists()
        return exists

    # 初期字幕データ一括投入（大）
    def download_channel_subtitles(self, channel_id: str) -> None:
        self.insert_initial_video_data(channel_id)

        default_audio_language, translation_languages = self.get_translation_info(channel_id)
        # TODO:字幕の追加状況確認メソッド追加
        # self.insert_or_update_latest_subtitle_info(channel_id)

        playlist_videos = VideoDetail.objects.filter(channel_id=channel_id)

        # ログ出力用
        total_videos = len(playlist_videos)
        processed_videos = 0

        for video in playlist_videos:
            video_id = video.video_id
            # 字幕IDが存在するかのチェックを行うデータ準備
            subtitle_ids = [generate_subtitle_id(video_id, SubtitleType.AUTOMATIC, default_audio_language)]
            for language in translation_languages:
                subtitle_ids.append(generate_subtitle_id(video_id, SubtitleType.MANUAL, language))
            # TODO:自動字幕と手動字幕で登録するかしないかを分けるべき
            # 既に登録されているかのチェック
            existing_subtitle_info = self.check_subtitle_existence(video_id, subtitle_ids)

            # 既に処理を行っている場合実行しない
            if not existing_subtitle_info:
                self.download_video_subtitle(video_id, default_audio_language, translation_languages)
            else:
                logging.debug(f"{video_id}:登録済み")

            # 処理されたビデオ数を更新
            processed_videos += 1
            # 経過率をデバッグに出力
            logging.info(f"処理進行状況: {processed_videos}/{total_videos}")

    def check_subtitle_existence(self, video_id, subtitle_ids):
        """
        指定された video_id と複数の subtitle_ids を持つサブタイトルがすべて存在するかどうかを確認します。

        :param video_id: ビデオのID
        :param subtitle_ids: 確認したいサブタイトルのIDのリスト
        :return: すべてのサブタイトルが存在する場合は True、少なくとも1つでも存在しない場合は False
        """
        # ビデオIDに基づいてすべてのサブタイトル情報を取得します
        existing_subtitle_info = VideoSubtitleInfo.objects.filter(
            video_id=video_id
        )

        # 各 subtitle_id をチェックします
        for subtitle_id in subtitle_ids:
            # 指定された subtitle_id を持つレコードが存在するかどうかを確認します
            subtitle_exists = any(subtitle_info.subtitle_id == subtitle_id for subtitle_info in existing_subtitle_info)

            # もし存在しない subtitle_id が見つかれば False を返します
            if not subtitle_exists:
                return False

        # すべての subtitle_id が見つかった場合に True を返します
        return True

    def download_video_subtitle(self, video_id: str,
                                default_audio_language: YouTubeLanguage,
                                translation_languages: List[YouTubeLanguage]) -> None:

        # subtitle_info = self.youtube_subtitle_logic.download_subtitles_info(video_id)
        # FileHandler.write_json(subtitle_info, TEST_DIR+"subtitle_data/", video_id, )
        # return
        # TODO:データを事前に用意している場合は以下を使用
        subtitle_info = FileHandler.get_json_response(TEST_DIR + "subtitle_data/" + video_id)
        # TODO:自動字幕は一旦取得しないようにコメントアウト（量が多すぎる）
        # # 自動生成字幕
        # self.create_or_update_video_subtitle_info(video_id, subtitle_info, SubtitleType.AUTOMATIC,
        #                                           default_audio_language)
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
        # 既に登録されているかのチェック
        existing_subtitle_info = VideoSubtitleInfo.objects.filter(
            subtitle_id=generate_subtitle_id(video_id, subtitle_type, language),
        ).first()

        # ビデオサブタイトル情報が存在しない場合に新しいレコードを作成
        if not existing_subtitle_info:
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


class TestYoutubeDownloadService(unittest.TestCase):
    def setUp(self):
        # テスト前の準備
        self.youtube_download_service = YoutubeDownloadService()

    def test_download_video_subtitle(self):
        video_id = TEST_YOUTUBE_VIDEO_ID
        default_audio_language = YouTubeLanguage.KOREAN
        translation_language = YouTubeLanguage.JAPANESE

        self.youtube_download_service.download_video_subtitle(video_id, default_audio_language, translation_language)

# if __name__ == '__main__':
#     unittest.main()
