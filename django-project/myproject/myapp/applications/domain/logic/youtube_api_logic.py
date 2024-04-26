# 必要なモジュールをインポート
import unittest

from myapp.applications.infrastructure.repository.web_client import WebClient
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myapp.applications.util.file_handler import FileHandler
from myproject.settings.base import YOUTUBE_API_KEY, TEST_YOUTUBE_VIDEO_ID, TEST_YOUTUBE_CHANNEL_ID, \
    TEST_YOUTUBE_PLAYLIST_ID


# YouTubeのAPIを操作するクラス
class YouTubeApiLogic:
    def __init__(self):
        # YouTubeのAPIキーを読み込む
        self.api_key = YOUTUBE_API_KEY
        # YouTubeのAPIのベースURL
        self.base_url = "https://www.googleapis.com/youtube/v3/"

    # 動画の詳細を取得するメソッド
    def get_video_details(self, video_id, language=YouTubeLanguage.ENGLISH):
        # APIのエンドポイントURLを設定
        api_url = self.base_url + "videos"

        # リクエストパラメータを設定
        params = {
            'id': video_id,
            'key': self.api_key,
            'part': 'snippet,liveStreamingDetails,localizations',
            'hl': language.value  # 言語を指定するパラメータを追加
        }

        # WebClientクラスを使ってAPIリクエストを送信し、レスポンスを取得
        return WebClient.make_api_request(api_url, params)

    # チャンネルの詳細を取得するメソッド
    def get_channel_details(self, channel_id, language=YouTubeLanguage.ENGLISH):
        # APIのエンドポイントURLを設定
        api_url = self.base_url + "channels"

        # リクエストパラメータを設定
        params = {
            'id': channel_id,
            'key': self.api_key,
            'part': 'snippet',
            'hl': language.value  # 言語を指定するパラメータを追加
        }

        # WebClientクラスを使ってAPIリクエストを送信し、レスポンスを取得
        return WebClient.make_api_request(api_url, params)

    # プレイリスト内の全ての動画を取得するメソッド
    def get_all_playlist_videos(self, playlist_id, language=YouTubeLanguage.ENGLISH):
        all_videos = []
        next_page_token = None

        # ページングを考慮してプレイリスト内の全ての動画を取得
        while True:
            response = self.get_playlist_videos_page(playlist_id, next_page_token, language=language)
            if response is not None:
                all_videos.extend(response.get("items", []))
                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break
            else:
                break

        return all_videos

    # プレイリスト内の動画をページングしながら取得するメソッド
    def get_playlist_videos_page(self, playlist_id, page_token=None, language=YouTubeLanguage.ENGLISH):
        # APIのエンドポイントURLを設定
        api_url = self.base_url + "playlistItems"

        # リクエストパラメータを設定
        params = {
            'playlistId': playlist_id,
            'key': self.api_key,
            'part': 'snippet',
            'maxResults': 50,
            'hl': language.value  # 言語を指定するパラメータを追加
        }

        # ページングのトークンを設定
        if page_token:
            params['pageToken'] = page_token

        # WebClientクラスを使ってAPIリクエストを送信し、レスポンスを取得
        return WebClient.make_api_request(api_url, params)

    # 動画の字幕情報を取得するメソッド
    def get_video_captions(self, video_id):
        try:
            # APIのエンドポイントURLを設定
            api_url = self.base_url + "captions"

            # リクエストパラメータを設定
            params = {
                'videoId': video_id,
                'key': self.api_key,
                'part': 'snippet',
            }

            # WebClientクラスを使ってAPIリクエストを送信し、レスポンスを取得
            captions_response = WebClient.make_api_request(api_url, params)

            # 字幕情報を返す
            return captions_response

        except Exception as e:
            print('An error occurred:', str(e))


# YouTubeApiLogicクラスのテスト
class TestYouTubeApiLogic(unittest.TestCase):
    def setUp(self):
        # テスト前の準備
        self.youtube_logic = YouTubeApiLogic()

    # 動画の詳細を取得するメソッドのテスト
    def test_get_video_details(self):
        # テスト用の動画IDを指定
        video_id = TEST_YOUTUBE_VIDEO_ID
        # 動画の詳細を取得
        video_details = self.youtube_logic.get_video_details(video_id, language=YouTubeLanguage.JAPANESE)
        # 取得した動画の詳細を出力
        FileHandler.format_json_print(video_details)

    # チャンネルの詳細を取得するメソッドのテスト
    def test_get_channel_details(self):
        # テスト用のチャンネルIDを指定
        channel_id = TEST_YOUTUBE_CHANNEL_ID
        # チャンネルの詳細を取得
        channel_details = self.youtube_logic.get_channel_details(channel_id, language=YouTubeLanguage.JAPANESE)
        # 取得したチャンネルの詳細を出力
        FileHandler.format_json_print(channel_details)

    # プレイリスト内の全ての動画を取得するメソッドのテスト
    def test_get_all_playlist_videos(self):
        # テスト用のプレイリストIDを指定
        playlist_id = TEST_YOUTUBE_PLAYLIST_ID
        # プレイリスト内の全ての動画を取得
        playlist_videos = self.youtube_logic.get_all_playlist_videos(playlist_id, language=YouTubeLanguage.JAPANESE)
        # 取得したプレイリストの動画を出力
        FileHandler.format_json_print(playlist_videos)

    # 動画の字幕情報を取得するメソッドのテスト
    def test_get_video_captions(self):
        # テスト用の動画IDを指定
        video_id = TEST_YOUTUBE_VIDEO_ID
        # 動画の字幕情報を取得
        captions_info = self.youtube_logic.get_video_captions(video_id)
        # 取得した字幕情報を出力
        FileHandler.format_json_print(captions_info)

# if __name__ == '__main__':
#     # テストを実行
#     unittest.main()
