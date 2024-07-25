# 必要なモジュールをインポート
import functools
import logging
import unittest
from datetime import datetime

import googleapiclient.discovery
from django.conf import settings
from googleapiclient.errors import HttpError

from myapp.applications.domain.logic.database_common_logic import DatabaseCommonLogic
from myapp.applications.util.code.subtitle_status import SubtitleStatus
from myapp.applications.util.code.subtitle_type import SubtitleType
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myapp.applications.util.file_handler import FileHandler
from myproject.settings.base import YOUTUBE_API_KEY, TEST_YOUTUBE_VIDEO_ID, TEST_YOUTUBE_CHANNEL_ID, \
    TEST_YOUTUBE_PLAYLIST_ID, YOUTUBE_API_KEY_1, YOUTUBE_API_KEY_2, YOUTUBE_API_KEY_3, YOUTUBE_API_KEY_4, TEST_DIR


# YouTubeのAPIを操作するクラス
class YouTubeApiLogic:
    def __init__(self):
        self.database_common_logic = DatabaseCommonLogic()
        # YouTubeのAPIキーを読み込む
        # APIキーをリストに登録
        self.api_keys = []
        self.api_keys.append(YOUTUBE_API_KEY)
        self.api_keys.append(YOUTUBE_API_KEY_1)
        self.api_keys.append(YOUTUBE_API_KEY_2)
        self.api_keys.append(YOUTUBE_API_KEY_3)
        self.api_keys.append(YOUTUBE_API_KEY_4)
        self.api_key_index = 0

    @staticmethod
    def retry_on_quota_exceeded(function):
        @functools.wraps(function)
        def wrapper(self, *args, **kwargs):
            """
            リトライ処理を行う内部メソッド
            """
            while self.api_key_index < len(self.api_keys):
                try:
                    # functionを実行
                    return function(self, *args, **kwargs)
                except HttpError as e:
                    logging.debug('エラーの種類: %s', type(e).__name__)
                    logging.debug(f"{self.api_key_index}個目のAPI KEY")
                    logging.error('エラーが発生しました: %s', str(e))
                    # エラー詳細を確認して、quotaExceeded かどうかを検証する
                    error_details = e.error_details
                    for error_detail in error_details:
                        if 'quotaExceeded' in error_detail.get('reason', ''):
                            logging.error('エラーが発生しました（quotaExceeded）: %s', str(e))
                            # quotaExceeded エラーが見つかった場合は次のAPIキーに切り替えてリトライする
                            self.api_key_index += 1
                            break
                    else:
                        logging.error('その他のエラーが発生しました（HttpErrorその他）: %s', str(e))
                        # quotaExceeded エラーが見つからなかった場合
                        raise RuntimeError(str(e))  # RuntimeError などの組み込みの例外クラスを使用する
                except Exception as e:
                    # その他のすべてのエラーに対してもログを出力してリトライしない
                    logging.debug('エラーの種類: %s', type(e).__name__)
                    logging.debug(f"{self.api_key_index}個目のAPI KEY")
                    logging.error('その他のエラーが発生しました: %s', str(e))
                    raise RuntimeError(str(e))  # RuntimeError などの組み込みの例外クラスを使用する
            raise RuntimeError("リトライ回数越えエラー")  # RuntimeError などの組み込みの例外クラスを使用する

        return wrapper

    # 動画の詳細を取得するメソッド
    @retry_on_quota_exceeded
    def get_video_details(self, video_id):
        # YouTube Data APIを使用して動画情報を取得する
        youtube = googleapiclient.discovery.build(
            'youtube', 'v3', developerKey=self.api_keys[self.api_key_index])
        request = youtube.videos().list(
            part="snippet,liveStreamingDetails,localizations",
            id=video_id,
        )
        response = request.execute()
        return response

    def get_video_details_data(self, video_id):
        response = self.get_video_details(video_id)
        video_data = {}
        items = response.get('items')
        if items:
            item = items[0]
            snippet = item.get('snippet', {})
            video_data['video_id'] = item.get('id')
            video_data['e_tag'] = response.get('etag')
            video_data['title'] = snippet.get('title')
            video_data['published_at'] = snippet.get('publishedAt')
            video_data['description'] = snippet.get('description')
            thumbnail_info = snippet.get('thumbnails', {}).get('default', {})
            video_data['thumbnail'] = thumbnail_info.get('url')
            video_data['channel_id'] = snippet.get('channelId')
            video_data['default_language'] = snippet.get('defaultLanguage')

            # 存在しない場合はNoneを指定
            live_streaming_details = item.get('liveStreamingDetails', {})
            video_data['default_audio_language'] = live_streaming_details.get('defaultLanguage')
            video_data['actual_start_time'] = live_streaming_details.get('actualStartTime')
            video_data['actual_end_time'] = live_streaming_details.get('actualEndTime')
            video_data['scheduled_start_time'] = live_streaming_details.get('scheduledStartTime')

            # ローカライズされた情報を取得
            localized_data = snippet.get('localized', {})
            video_data['localized'] = {'title': localized_data.get('title'),
                                       'description': localized_data.get('description')}

            localizations_datas = item.get('localizations', {})
            localizations_data_list = []
            for language_code, localizations_data in localizations_datas.items():
                localizations_data_list.append({
                    'language_code': language_code,
                    'title': localizations_data.get('title'),
                    'description': localizations_data.get('description')
                })
            video_data['localizations_data'] = localizations_data_list

        return video_data

    # チャンネルの詳細を取得するメソッド
    @retry_on_quota_exceeded
    def get_channel_details(self, channel_id):
        # YouTube Data APIを使用してチャンネル情報を取得する
        youtube = googleapiclient.discovery.build(
            'youtube', 'v3', developerKey=self.api_keys[self.api_key_index])
        request = youtube.channels().list(
            part="snippet,contentDetails",
            id=channel_id,
        )
        response = request.execute()
        return response

    def get_channel_details_data(self, channel_id):
        response = self.get_channel_details(channel_id)
        channel_data = {}

        if response.get('items'):
            item = response.get('items')[0]
            # チャンネルID
            channel_data['channel_id'] = item.get('id')
            # チャンネルプレイリストID
            channel_data['playlist_id'] = item.get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads')
            # チャンネルタイトル
            channel_data['title'] = item.get('snippet', {}).get('title')
            # チャンネルの説明
            channel_data['description'] = item.get('snippet', {}).get('description')
            # カスタムURL
            channel_data['custom_url'] = item.get('snippet', {}).get('customUrl')
            # 公開日時
            channel_data['published_at'] = item.get('snippet', {}).get('publishedAt')
            # サムネイルURL
            channel_data['thumbnail'] = item.get('snippet', {}).get('thumbnails', {}).get('high', {}).get('url')
            # 国コード
            channel_data['country'] = item.get('snippet', {}).get('country')

            # ローカライズされた情報を取得
            localized_data = item.get('snippet', {}).get('localized', [])
            localized_list = []
            localized_list.append(
                {'title': localized_data.get('title'), 'description': localized_data.get('description')})
            channel_data['localized'] = localized_list

        return channel_data

    # プレイリスト内の全ての動画を取得するメソッド
    def get_all_playlist_videos(self, playlist_id):
        all_videos = []
        next_page_token = None

        # ページングを考慮してプレイリスト内の全ての動画を取得
        while True:
            response = self.get_playlist_videos_page(playlist_id, next_page_token)
            if response is not None:
                all_videos.extend(response.get("items", []))
                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break
            else:
                break

        return all_videos

    # プレイリスト内の動画をページングしながら取得するメソッド
    @retry_on_quota_exceeded
    def get_playlist_videos_page(self, playlist_id, page_token=None):
        # YouTube Data APIを使用してプレイリスト内の動画情報を取得する
        youtube = googleapiclient.discovery.build(
            'youtube', 'v3', developerKey=self.api_keys[self.api_key_index])
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=page_token,
        )
        response = request.execute()
        return response

    def get_channel_videos(self, playlist_id):
        playlist_data = self.get_all_playlist_videos(playlist_id)
        videos = []

        for item in playlist_data:
            video_id = item.get("contentDetails", {}).get("videoId")
            e_tag = item.get("etag", {})
            title = item.get("snippet", {}).get("title")
            published_at = item.get("snippet", {}).get("publishedAt")
            description = item.get("snippet", {}).get("description")
            thumbnail = self.get_thumbnail_url(item)
            channel_id = item.get("snippet", {}).get("channelId")
            channel_title = item.get("snippet", {}).get("channelTitle")

            # 他の項目も含める

            if video_id:
                videos.append({
                    "video_id": video_id,
                    "e_tag": e_tag,
                    "title": title,
                    "published_at": published_at,
                    "description": description,
                    "thumbnail": thumbnail,
                    "channel_id": channel_id,
                    "channel_title": channel_title,
                    # 他の情報もここで追加する
                })

        return videos

    def get_thumbnail_url(self, item):
        snippet = item.get("snippet", {})
        thumbnails = snippet.get("thumbnails", {})

        maxres = thumbnails.get("maxres", {}).get("url")
        if maxres:
            return maxres

        standard = thumbnails.get("standard", {}).get("url")
        if standard:
            return standard

        high = thumbnails.get("high", {}).get("url")
        if high:
            return high

        medium = thumbnails.get("medium", {}).get("url")
        if medium:
            return medium

        default = thumbnails.get("default", {}).get("url")
        if default:
            return default

        return None  # サムネイルが全て存在しない場合

    # 動画の字幕情報を取得するメソッド
    @retry_on_quota_exceeded
    def get_video_captions(self, video_id):
        # YouTube Data APIを使用して動画の字幕情報を取得する
        youtube = googleapiclient.discovery.build(
            'youtube', 'v3', developerKey=self.api_keys[self.api_key_index])
        request = youtube.captions().list(
            part="snippet",
            videoId=video_id
        )
        response = request.execute()
        return response

    # 動画の字幕情報を取得するメソッド
    def get_subtitle_info(self, video_id, default_audio_language, translation_languages):
        response = self.get_video_captions(video_id)
        subtitle_info_list = []

        if response.get('items'):
            for item in response.get('items'):
                subtitle_info = {}
                language = item.get('snippet', {}).get('language')
                # 字幕の言語が default_audio_language または translation_languages に含まれている場合のみ
                if language == default_audio_language.value or language in [lang.value for lang in
                                                                            translation_languages]:
                    # 動画ID
                    subtitle_info['video_id'] = item.get('snippet', {}).get('videoId')
                    # 最終更新日
                    subtitle_info['last_updated'] = item.get('snippet', {}).get('lastUpdated')
                    # 字幕種別
                    track_kind = item.get('snippet', {}).get('trackKind')
                    subtitle_info[
                        'subtitle_type'] = SubtitleType.AUTOMATIC if track_kind == 'asr' else SubtitleType.MANUAL
                    # 字幕言語
                    subtitle_info['language'] = YouTubeLanguage(language)
                    subtitle_info_list.append(subtitle_info)

                else:
                    try:
                        YouTubeLanguage(language)
                    except ValueError:
                        # ログファイルに記録を残す
                        # エラーを特定のファイルに記録
                        error_message = f"{datetime.now()} - Enumに当てはまらない文字列: {language}"
                        FileHandler.append_to_file(error_message, TEST_DIR, "error_enum.txt")
                        logging.error(f"Enumに当てはまらない文字列: {language}")
        return subtitle_info_list

    def update_video_caption(self, video_id, default_audio_language, translation_languages):
        video_captions = self.get_subtitle_info(video_id, default_audio_language,
                                                translation_languages)
        for video_caption in video_captions:
            self.database_common_logic.insert_or_update_video_subtitle_info(video_id,
                                                                            video_caption.get('subtitle_type'),
                                                                            video_caption.get('language'),
                                                                            SubtitleStatus.UNREGISTERED,
                                                                            video_caption.get('last_updated'))

        # 自動字幕の情報追加
        self.database_common_logic.insert_false_subtitle_info(video_id, SubtitleType.AUTOMATIC, default_audio_language)
        self.database_common_logic.insert_false_subtitle_info(video_id, SubtitleType.MANUAL, default_audio_language)
        # 手動字幕の情報追加
        for language in translation_languages:
            self.database_common_logic.insert_false_subtitle_info(video_id, SubtitleType.MANUAL, language)

    # 動画のカテゴリ情報を取得する
    @retry_on_quota_exceeded
    def get_video_category(self, category_id):
        # YouTube Data APIを使用して動画カテゴリを取得する
        youtube = googleapiclient.discovery.build(
            'youtube', 'v3', developerKey=self.api_keys[self.api_key_index])
        request = youtube.videoCategories().list(
            part="snippet",
            id=category_id
        )
        response = request.execute()
        return response

    @retry_on_quota_exceeded
    def get_youtube_languages(self):
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=self.api_keys[self.api_key_index])

        request = youtube.i18nLanguages().list(part='snippet')
        response = request.execute()

        language_codes = [item['snippet']['hl'] for item in response['items']]
        return language_codes


# YouTubeApiLogicクラスのテスト
class TestYouTubeApiLogic(unittest.TestCase):
    def setUp(self):
        # テスト前の準備
        self.youtube_logic = YouTubeApiLogic()
        settings.configure()

    # 動画の詳細を取得するメソッドのテスト
    def test_get_video_details(self):
        # テスト用の動画IDを指定
        video_id = TEST_YOUTUBE_VIDEO_ID
        # 動画の詳細を取得
        video_details = self.youtube_logic.get_video_details(video_id)
        # 取得した動画の詳細を出力
        FileHandler.format_json_print(video_details)
        FileHandler.write_json_response(video_details)

    def test_get_video_details_data(self):
        # テスト用の動画IDを指定
        video_id = TEST_YOUTUBE_VIDEO_ID
        # 動画の詳細を取得
        video_details = self.youtube_logic.get_video_details_data(video_id)
        # 取得した動画の詳細を出力
        FileHandler.format_json_print(video_details)
        FileHandler.write_json_response(video_details)

    # チャンネルの詳細を取得するメソッドのテスト
    def test_get_channel_details(self):
        # テスト用のチャンネルIDを指定
        channel_id = TEST_YOUTUBE_CHANNEL_ID
        # チャンネルの詳細を取得
        channel_details = self.youtube_logic.get_channel_details(channel_id)
        # 取得したチャンネルの詳細を出力
        FileHandler.format_json_print(channel_details)
        FileHandler.write_json_response(channel_details)

    # プレイリスト内の全ての動画を取得するメソッドのテスト
    def test_get_all_playlist_videos(self):
        # テスト用のプレイリストIDを指定
        playlist_id = TEST_YOUTUBE_PLAYLIST_ID
        # プレイリスト内の全ての動画を取得
        playlist_videos = self.youtube_logic.get_all_playlist_videos(playlist_id)
        # 取得したプレイリストの動画を出力
        FileHandler.format_json_print(playlist_videos)
        FileHandler.write_json_response(playlist_videos)

    # 動画の字幕情報を取得するメソッドのテスト
    def test_get_video_captions(self):
        # テスト用の動画IDを指定
        video_id = TEST_YOUTUBE_VIDEO_ID
        # 動画の字幕情報を取得
        captions_info = self.youtube_logic.get_video_captions(video_id)
        # 取得した字幕情報を出力
        FileHandler.format_json_print(captions_info)

    # 動画のカテゴリ情報を取得するテスト
    def test_get_video_category(self):
        # カテゴリIDを指定
        category_id = 10
        # 動画のカテゴリ情報を取得
        category_info = self.youtube_logic.get_video_category(category_id)
        # 取得した字幕情報を出力
        FileHandler.format_json_print(category_info)

    def test_get_channel_videos(self):
        # テスト用のチャンネルIDを指定
        channel_id = TEST_YOUTUBE_CHANNEL_ID
        # チャンネルの動画一覧を取得
        playlist_id = self.youtube_logic.get_channel_details_data(channel_id).get('playlist_id')
        playlist_videos = self.youtube_logic.get_channel_videos(playlist_id)
        # 取得したチャンネルの詳細を出力
        print(playlist_videos)

    def test_get_channel_details_data(self):
        # テスト用のチャンネルIDを指定
        channel_id = TEST_YOUTUBE_CHANNEL_ID
        # チャンネルの詳細を取得
        result = self.youtube_logic.get_channel_details_data(channel_id)
        # 取得したチャンネルの詳細を出力
        FileHandler.format_json_print(result)
        FileHandler.write_json_response(result)

    def test_get_subtitle_info(self):
        # テスト用の動画IDを指定
        video_id = TEST_YOUTUBE_VIDEO_ID
        # 動画の字幕情報を取得
        captions_info = self.youtube_logic.get_subtitle_info(video_id)
        # 取得した字幕情報を出力
        print(captions_info)
        # Enumを扱っているためjsonにできない
        # FileHandler.format_json_print(captions_info)

    def test_get_youtube_languages(self):
        result = self.youtube_logic.get_youtube_languages()
        FileHandler.format_json_print(result)

# if __name__ == '__main__':
#     # テストを実行
#     unittest.main()
