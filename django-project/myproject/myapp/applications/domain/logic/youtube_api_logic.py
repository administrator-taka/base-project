# 必要なモジュールをインポート
import unittest

import googleapiclient.discovery
from django.conf import settings

from myapp.applications.util.file_handler import FileHandler
from myproject.settings.base import YOUTUBE_API_KEY, TEST_YOUTUBE_VIDEO_ID, TEST_YOUTUBE_CHANNEL_ID, \
    TEST_YOUTUBE_PLAYLIST_ID


# YouTubeのAPIを操作するクラス
class YouTubeApiLogic:
    def __init__(self):
        # YouTubeのAPIキーを読み込む
        self.api_key = YOUTUBE_API_KEY

    # 動画の詳細を取得するメソッド
    def get_video_details(self, video_id):
        try:
            # YouTube Data APIを使用して動画情報を取得する
            youtube = googleapiclient.discovery.build(
                'youtube', 'v3', developerKey=self.api_key)
            request = youtube.videos().list(
                part="snippet,liveStreamingDetails,localizations",
                id=video_id,
            )
            response = request.execute()
            return response
        except Exception as e:
            print('An error occurred:', str(e))
            return None

    # チャンネルの詳細を取得するメソッド
    def get_channel_details(self, channel_id):
        try:
            # YouTube Data APIを使用してチャンネル情報を取得する
            youtube = googleapiclient.discovery.build(
                'youtube', 'v3', developerKey=self.api_key)
            request = youtube.channels().list(
                part="snippet,contentDetails",
                id=channel_id,
            )
            response = request.execute()
            return response
        except Exception as e:
            print('An error occurred:', str(e))
            return None

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
    def get_playlist_videos_page(self, playlist_id, page_token=None):
        try:
            # YouTube Data APIを使用してプレイリスト内の動画情報を取得する
            youtube = googleapiclient.discovery.build(
                'youtube', 'v3', developerKey=self.api_key)
            request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=page_token,
            )
            response = request.execute()
            return response
        except Exception as e:
            print('An error occurred:', str(e))
            return None

    def get_channel_id_playlist_id(self, channel_id):
        channel_details = self.get_channel_details(channel_id)
        playlist_id = channel_details["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        return playlist_id

    def get_channel_videos(self, playlist_id):
        playlist_data = self.get_all_playlist_videos(playlist_id)
        videos = []

        for item in playlist_data:
            video_id = item.get("contentDetails", {}).get("videoId")
            e_tag = item.get("etag", {})
            title = item.get("snippet", {}).get("title")
            published_at = item.get("snippet", {}).get("publishedAt")
            description = item.get("snippet", {}).get("description")
            thumbnail = item.get("snippet", {}).get("thumbnails", {}).get("high", {}).get("url")
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

    # 動画の字幕情報を取得するメソッド
    def get_video_captions(self, video_id):
        try:
            # YouTube Data APIを使用して動画の字幕情報を取得する
            youtube = googleapiclient.discovery.build(
                'youtube', 'v3', developerKey=self.api_key)
            request = youtube.captions().list(
                part="snippet",
                videoId=video_id
            )
            response = request.execute()
            return response
        except Exception as e:
            print('An error occurred:', str(e))
            return None

    # 動画のカテゴリ情報を取得する
    def get_video_category(self, category_id):
        try:
            # YouTube Data APIを使用して動画カテゴリを取得する
            youtube = googleapiclient.discovery.build(
                'youtube', 'v3', developerKey=self.api_key)
            request = youtube.videoCategories().list(
                part="snippet",
                id=category_id
            )
            response = request.execute()
            return response
        except Exception as e:
            print('An error occurred:', str(e))
            return None


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
        playlist_id = self.youtube_logic.get_channel_id_playlist_id(channel_id)
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

# if __name__ == '__main__':
#     # テストを実行
#     unittest.main()
