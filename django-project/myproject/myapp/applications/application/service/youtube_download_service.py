import collections
import datetime
import logging
import time
import unittest
from datetime import datetime
from typing import List

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Prefetch, OuterRef, Exists

from myapp.applications.domain.logic.chat_gpt_api_logic import ChatGPTApiLogic
from myapp.applications.domain.logic.natural_language_processing_logic import NaturalLanguageProcessingLogic
from myapp.applications.domain.logic.youtube_api_logic import YouTubeApiLogic
from myapp.applications.domain.logic.youtube_subtitle_logic import YouTubeSubtitleLogic
from myapp.applications.util.code.learning_status import LearningStatus
from myapp.applications.util.code.subtitle_status import SubtitleStatus
from myapp.applications.util.code.subtitle_type import SubtitleType
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myapp.applications.util.file_handler import FileHandler
from myapp.applications.util.pagination_info import PaginationInfo
from myapp.applications.util.util_generate import generate_subtitle_id, generate_uuid
from myapp.models import VideoSubtitleInfo, VideoSubtitle, SubtitleTranslation, ChannelDetail, VideoDetail, \
    ChannelTranslationInfo, SubtitleLearningMemory
from myproject.settings.base import TEST_YOUTUBE_VIDEO_ID, TEST_DIR


class YoutubeDownloadService:
    def __init__(self):
        self.youtube_subtitle_logic = YouTubeSubtitleLogic()
        self.youtube_api_logic = YouTubeApiLogic()
        self.chatgpt_api_logic = ChatGPTApiLogic()
        self.nlp_logic = NaturalLanguageProcessingLogic()

    def execute_chatgpt_translation(self, subtitle_text_id, language, call_api=False):
        subtitle_translation = SubtitleTranslation.objects.get(
            subtitle_text_id=subtitle_text_id, language_code=language.value)

        subtitle_text = subtitle_translation.subtitle_text_id.subtitle_text
        subtitle_translation_text = subtitle_translation.subtitle_translation_text
        default_language = subtitle_translation.subtitle_text_id.subtitle_id.language_code
        request_path = f"resource/chatgpt_translation_prompt/from_{default_language}_to_{language.value}.txt"
        template = FileHandler.read_txt(request_path)
        # プレースホルダーに変数を代入する
        request = template.format(
            subtitle_text=subtitle_text,
            subtitle_translation_text=subtitle_translation_text,
            copy_code_block="コピーできるようにすべてコードブロックに出力してください。" if not call_api else ""
        )
        logging.debug(request)
        if call_api:
            response = self.chatgpt_api_logic.execute_chatgpt(request)
            logging.debug(request)
        else:
            response = None

        return {"request": request, "response": response}

    def get_activate_channel_list(self):
        channel_translation_infos = ChannelTranslationInfo.objects.filter(
        ).order_by('default_audio_language')

        channel_list = []
        for channel_translation_info in channel_translation_infos:
            channel_data = {
                'title': channel_translation_info.channel_id.title,
                'channel_id': channel_translation_info.channel_id.channel_id,
                'default_audio_language': channel_translation_info.default_audio_language,
                'translation_languages': channel_translation_info.translation_languages,
                'thumbnail': channel_translation_info.channel_id.thumbnail,
            }
            channel_list.append(channel_data)
        return channel_list

    def insert_or_update_subtitle_learning_memory(self, subtitle_text_id, language_code, learning_status):
        # 対象のSubtitleTranslationレコードを取得
        subtitle_translation = SubtitleTranslation.objects.get(
            subtitle_text_id=subtitle_text_id, language_code=language_code.value)

        # update_or_createメソッドを使用して、存在確認と更新または新規作成を行う
        SubtitleLearningMemory.objects.update_or_create(
            subtitle_translation_text_id=subtitle_translation,
            defaults={
                'learning_status': learning_status.value,
                'last_updated': datetime.now()
            }
        )

    def update_subtitle_translation(self, subtitle_text_id, language, subtitle_literal_translation_text,
                                    subtitle_translation_text_detail):
        subtitle_translation_info = SubtitleTranslation.objects.get(
            subtitle_text_id=subtitle_text_id, language_code=language.value)
        subtitle_translation_info.subtitle_literal_translation_text = subtitle_literal_translation_text
        subtitle_translation_info.subtitle_translation_text_detail = subtitle_translation_text_detail
        subtitle_translation_info.save()

    def get_subtitle_text_data(self, subtitle_text_id, language):
        subtitle_translation = SubtitleTranslation.objects.get(
            subtitle_text_id=subtitle_text_id, language_code=language.value)

        learning_memory = SubtitleLearningMemory.objects.filter(
            subtitle_translation_text_id=subtitle_translation).first()
        subtitle_text_data = {
            'video_id': subtitle_translation.subtitle_text_id.subtitle_id.video_id.video_id,
            'subtitle_text_id': subtitle_translation.subtitle_text_id.subtitle_text_id,
            't_start_ms': subtitle_translation.subtitle_text_id.t_start_ms,
            'subtitle_text': subtitle_translation.subtitle_text_id.subtitle_text,
            'subtitle_translation_text': subtitle_translation.subtitle_translation_text,
            'subtitle_literal_translation_text': subtitle_translation.subtitle_literal_translation_text,
            'subtitle_translation_text_detail': subtitle_translation.subtitle_translation_text_detail,
            'language_code': subtitle_translation.language_code,
            'last_updated': learning_memory.last_updated if learning_memory else None,
            'learning_status': learning_memory.learning_status if learning_memory else LearningStatus.NOT_CHECKED.value,
        }
        return subtitle_text_data

    def update_channel_translation_info(self, channel_id, default_audio_language, translation_languages):
        translation_info, created = ChannelTranslationInfo.objects.get_or_create(channel_id_id=channel_id)
        translation_info.default_audio_language = default_audio_language.value
        translation_info.translation_languages = [lang.value for lang in translation_languages]
        translation_info.save()

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
            self.update_video_caption(video_id, default_audio_language, translation_languages)
            # 処理されたビデオ数を更新
            processed_videos += 1
            # 経過率をデバッグに出力
            logging.info(f"処理進行状況: {processed_videos}/{total_videos}")

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
                "video_id": result.subtitle_id.video_id.video_id,
                "title": result.subtitle_id.video_id.title,
                "t_start_ms": result.t_start_ms,
                "subtitle_text": result.subtitle_text,
                "youtube_url": f"https://www.youtube.com/watch?v={result.subtitle_id.video_id_id}&t={result.t_start_ms}ms"
            }
            search_results.append(result_dict)

        return search_results

    # 単語検索
    def search_multiple_word(self, search_word, channel_id=None, subtitle_type=None, language_code=None):
        # VideoDetailをベースにクエリを構築
        queryset = VideoDetail.objects.filter(
            channel_id=channel_id
        ).order_by('published_at')

        # PrefetchでSubtitleTranslationとSubtitleLearningMemoryを取得
        queryset = queryset.prefetch_related(
            Prefetch('videosubtitleinfo_set',
                     queryset=VideoSubtitleInfo.objects.filter(
                         subtitle_type=subtitle_type.value
                     ).prefetch_related(
                         Prefetch('videosubtitle_set',
                                  queryset=VideoSubtitle.objects.all().order_by('t_start_ms', 't_offset_ms'))
                     ))
        )

        # 結果を辞書のリストに詰めて返す
        search_results = []
        search_word_list = search_word.split()
        n = len(search_word_list)
        logging.debug(f"検索開始")
        for video in queryset:
            logging.debug("★★★")
            # 翻訳データを取得して辞書に追加
            for info in video.videosubtitleinfo_set.all():
                subtitles = info.videosubtitle_set.all()
                full_text = ' '.join(subtitle.subtitle_text for subtitle in subtitles)

                # 検索語が結合テキストに含まれているか確認
                if search_word in full_text:
                    t_start_ms = ''
                    subtitle_text = ''
                    for i in range(n - 1, len(subtitles)):
                        target_word_list = [subtitles[i - (n - j - 1)].subtitle_text for j in range(n)]
                        target_word = ' '.join(target_word_list)

                        if target_word == search_word:
                            start = subtitles[i - (n - 1)]
                            end = subtitles[i]
                            logging.debug(
                                f"start!subtitle_id: {start.subtitle_id},subtitle_text: {start.subtitle_text},t_start_ms: {start.t_start_ms}, t_offset_ms: {start.t_offset_ms}")
                            logging.debug(
                                f"end!subtitle_id: {end.subtitle_id},subtitle_text: {end.subtitle_text},t_start_ms: {end.t_start_ms}, t_offset_ms: {end.t_offset_ms}")
                            t_start_ms = start.t_start_ms

                            # 追加: 特定範囲の字幕データを取得
                            subtitles_in_range = subtitles.filter(
                                subtitle_id=info.subtitle_id,
                                t_start_ms__gte=start.t_start_ms,
                                t_start_ms__lte=end.t_start_ms
                            ).order_by('t_start_ms', 't_offset_ms')

                            result = [subtitle.subtitle_text for subtitle in subtitles_in_range]
                            subtitle_text = ' '.join(result)
                            logging.debug(subtitle_text)
                    youtube_url = f"https://www.youtube.com/watch?v={video.video_id}&t={t_start_ms}ms"
                    result_dict = {
                        "video_id": video.video_id,
                        "title": video.title,
                        "t_start_ms": t_start_ms,
                        "subtitle_text": subtitle_text,
                        "youtube_url": youtube_url,
                    }
                    logging.debug(youtube_url)
                    search_results.append(result_dict)

        return search_results

    # 単語集計
    def calculate_word(self, channel_id, min_word, min_word_length, top_n, subtitle_type, stop_word_flag, lemmatize_flag):
        # チャンネルの翻訳情報を取得
        default_audio_language, translation_languages = self.get_translation_info(channel_id)

        # VideoDetailをベースにクエリを構築
        queryset = VideoDetail.objects.filter(
            channel_id=channel_id
        ).order_by('published_at')

        # PrefetchでSubtitleTranslationとSubtitleLearningMemoryを取得
        queryset = queryset.prefetch_related(
            Prefetch('videosubtitleinfo_set',
                     queryset=VideoSubtitleInfo.objects.filter(
                         subtitle_type=subtitle_type.value,
                         language_code=default_audio_language.value
                     ).prefetch_related(
                         Prefetch('videosubtitle_set',
                                  queryset=VideoSubtitle.objects.all().order_by('t_start_ms'))
                     ))
        )

        logging.debug(f"検索開始")
        all_words = []  # 全単語を収集するリストを初期化

        for video in queryset:
            logging.debug("★★★ Processing video ID: %s", video.video_id)

            for info in video.videosubtitleinfo_set.all():
                subtitles = info.videosubtitle_set.all()
                if not subtitles:  # subtitlesが空でないことを確認
                    continue
                if subtitle_type == SubtitleType.MANUAL:
                    # 重複チェック
                    if not self.check_duplicates(subtitles):
                        logging.debug(f"追加しない(重複チェック): {video.video_id}")
                        continue

                    # 階段チェック
                    if not self.check_staircase(subtitles):
                        logging.debug(f"追加しない(階段チェック): {video.video_id}")
                        continue

                # 各字幕テキストを単語に分割し、リストに追加
                info_words = []
                for subtitle in subtitles:
                    words = subtitle.subtitle_text.split()
                    # 単語の基本形に変換してリストに追加（フラグで制御）
                    if lemmatize_flag:
                        lemmatized_words = [self.nlp_logic.lemmatize_word(word) for word in words]
                    else:
                        lemmatized_words = words  # 基本形にしない場合はそのままの単語を使う
                    info_words.extend(lemmatized_words)

                # 単語の組み合わせを取得
                join_words = self.nlp_logic.get_combinations(info_words, min_word)
                all_words.extend(join_words)  # 各infoの単語を全単語リストに追加

        stop_words = self.nlp_logic.get_stop_words(default_audio_language) if stop_word_flag else set()
        filtered_words = self.nlp_logic.filter_words(all_words, min_word_length, stop_words)
        top_words_list = self.nlp_logic.calculate_word_frequencies(filtered_words, top_n)

        return top_words_list

    def check_duplicates(self, subtitles):
        all_subtitle_texts = [subtitle.subtitle_text for subtitle in subtitles]

        duplicate_check_list = collections.Counter(all_subtitle_texts)
        duplicate_ratio = len(duplicate_check_list) / len(all_subtitle_texts)
        logging.debug(f"{len(duplicate_check_list)}/{len(all_subtitle_texts)}={duplicate_ratio}")
        if duplicate_ratio < 0.5:
            return False
        return True

    def check_staircase(self, subtitles):
        current_subtitle_text = None
        count = 0
        continuous_count = 2

        for subtitle in subtitles:
            subtitle_text = subtitle.subtitle_text

            if current_subtitle_text and subtitle_text.startswith(current_subtitle_text):
                count += 1
                continuous_count = 0
            else:
                if continuous_count < 1:
                    count += 1
                continuous_count += 1

            current_subtitle_text = subtitle_text

        ratio = count / len(subtitles)
        logging.debug(f"{count}/{len(subtitles)}={ratio}")
        return ratio < 0.5

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

    def get_channel_data(self, channel_id):
        self.insert_channel_data(channel_id)
        # チャンネルIDに紐づくチャンネル情報を取得
        channel_detail = ChannelDetail.objects.filter(channel_id=channel_id).first()

        # チャンネル情報を辞書型に変換して返す
        if channel_detail:
            channel_translation_info = ChannelTranslationInfo.objects.filter(channel_id=channel_detail).first()
            channel_data = {
                'title': channel_detail.title,
                'description': channel_detail.description,
                'channel_id': channel_detail.channel_id,
                'playlist_id': channel_detail.playlist_id,
                'custom_url': channel_detail.custom_url,
                'published_at': channel_detail.published_at,
                'country': channel_detail.country,
                'default_audio_language': channel_translation_info.default_audio_language if channel_translation_info else None,
                'translation_languages': channel_translation_info.translation_languages if channel_translation_info else None,
                'thumbnail': channel_detail.thumbnail,
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
            if 'maxres' not in video_detail.thumbnail:
                video_detail.thumbnail = thumbnail
            video_detail.channel_id = ChannelDetail.objects.get(channel_id=channel_id)
            video_detail.e_tag = e_tag
            video_detail.save()
            logging.debug("動画情報が更新されました。")
        else:
            logging.debug("動画情報は既に最新です。")

    # 字幕のステータスの一覧を取得
    def get_channel_subtitle_list(self, channel_id, languages, page=1, page_size=10):
        # サブクエリのリストを生成
        subqueries = [
            # 各言語ごとの字幕情報をフィルタするサブクエリを生成
            VideoSubtitleInfo.objects.filter(
                video_id=OuterRef('pk'),  # 外部キー結合によって VideoDetail の主キーと結合
                language_code=language.value,  # 指定された言語の字幕情報を抽出
                subtitle_status=SubtitleStatus.REGISTERED.value,  # 登録済みの字幕を抽出
                subtitle_type=SubtitleType.MANUAL.value  # 手動で作成された字幕を抽出
            )
            for language in languages  # 言語リストの各言語に対してサブクエリを生成
        ]

        # 動的にフィルタ条件を生成
        filters = Q(channel_id=channel_id)  # チャンネルIDでフィルタリングする基本条件を設定
        for subquery in subqueries:  # 各言語のサブクエリを用いて動的にフィルタ条件を追加
            filters &= Exists(subquery)

        # フィルタ条件に合致する VideoDetail を取得
        video_details = VideoDetail.objects.filter(filters).distinct().order_by('-published_at')

        # ページごとのビデオ ID を取得
        paginator = Paginator(video_details, page_size)

        try:
            video_details_page = paginator.page(page)
        except PageNotAnInteger:
            video_details_page = paginator.page(1)
        except EmptyPage:
            video_details_page = paginator.page(paginator.num_pages)

        # ページごとのビデオごとの情報を取得してリストに追加
        video_list = []
        for video_detail in video_details_page.object_list:
            subtitle_infos = video_detail.videosubtitleinfo_set.all()
            subtitle_info_list = []
            for info in subtitle_infos:
                subtitle_info_list.append({
                    'language_code': info.language_code,
                    'subtitle_type': info.subtitle_type,
                    'subtitle_status': info.subtitle_status,
                })
            video_info = {
                'title': video_detail.title,
                'video_id': video_detail.video_id,
                'published_at': video_detail.published_at,
                'thumbnail': video_detail.thumbnail,
                'infos': subtitle_info_list
            }
            video_list.append(video_info)

        pagination_info = PaginationInfo(paginator, page, page_size)
        return {
            'video_list': video_list,
            'pagination_info': pagination_info.to_dict()
        }

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
                return

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
                target_subtitle = target_subtitles.filter(t_start_ms=base_subtitle.t_start_ms).first()
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

            # TODO:自動字幕と手動字幕で登録するかしないかを分けるべき
            # 既に登録されているかのチェック
            existing_subtitle_info = self.check_subtitle_existence(video_id, default_audio_language,
                                                                   translation_languages)

            # 既に処理を行っている場合実行しない
            if not existing_subtitle_info:
                self.download_video_subtitle(video_id, default_audio_language, translation_languages)
            else:
                logging.debug(f"{video_id}:登録済み")

            # 処理されたビデオ数を更新
            processed_videos += 1
            # 経過率をデバッグに出力
            logging.info(f"処理進行状況: {processed_videos}/{total_videos}")

    def single_download_video_subtitle(self, video_id):
        video_detail = VideoDetail.objects.get(video_id=video_id)
        default_audio_language, translation_languages = self.get_translation_info(video_detail.channel_id)
        self.download_video_subtitle(video_id, default_audio_language, translation_languages)

    def check_subtitle_existence(self, video_id, default_audio_language, translation_languages):
        # 字幕IDが存在するかのチェックを行うデータ準備
        subtitle_ids = [generate_subtitle_id(video_id, SubtitleType.MANUAL, default_audio_language),
                        generate_subtitle_id(video_id, SubtitleType.AUTOMATIC, default_audio_language)]
        for language in translation_languages:
            subtitle_ids.append(generate_subtitle_id(video_id, SubtitleType.MANUAL, language))
        # ビデオIDに基づいて指定されたsubtitle_idsを持つサブタイトル情報を取得します
        existing_subtitle_info = VideoSubtitleInfo.objects.filter(
            video_id=video_id,
            subtitle_id__in=subtitle_ids
        )

        # subtitle_statusがUNREGISTEREDのものがあればFalseを返します
        for subtitle_info in existing_subtitle_info:
            print(subtitle_info.subtitle_status)
            if SubtitleStatus(subtitle_info.subtitle_status) == SubtitleStatus.UNREGISTERED:
                logging.debug(f"{subtitle_info.subtitle_status}:字幕未取得")
                return False
        # 取得したsubtitle_idsをセットに変換して存在チェックを行います
        existing_subtitle_ids = set(existing_subtitle_info.values_list('subtitle_id', flat=True))

        # すべてのsubtitle_idがexisting_subtitle_idsに含まれているかをチェックします
        if not set(subtitle_ids).issubset(existing_subtitle_ids):
            return False

        # 全ての条件を満たす場合にTrueを返します
        return True

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

    def delete_channel_data(self, channel_id):
        ChannelDetail.objects.filter(channel_id=channel_id).delete()


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
