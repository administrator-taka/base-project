import unittest

import requests

from myapp.applications.util.file_handler import FileHandler
from myproject.settings.base import TEST_YOUTUBE_CHANNEL_ID, TEST_YOUTUBE_VIDEO_ID


class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/youtube_app/"

    def test_get_channel_data(self):
        channel_id = TEST_YOUTUBE_CHANNEL_ID
        url = f"{self.base_url}channel/{channel_id}"
        response = requests.get(url)
        FileHandler.format_json_print(response.json())

    def test_get_channel_video_list(self):
        channel_id = TEST_YOUTUBE_CHANNEL_ID
        url = f"{self.base_url}channel/{channel_id}/get_channel_video_list"
        response = requests.get(url, params={'page': 1, 'page_size': 10})  # ページ番号とページサイズを指定します
        FileHandler.format_json_print(response.json())

    def test_download_channel_subtitles(self):
        channel_id = TEST_YOUTUBE_CHANNEL_ID
        url = f"{self.base_url}channel/{channel_id}/download_channel_subtitles"
        response = requests.get(url)
        FileHandler.format_json_print(response.json())

    def test_search_word(self):
        channel_id = TEST_YOUTUBE_CHANNEL_ID
        url = f"{self.base_url}channel/{channel_id}/search_word"
        data = {"search_word": "인터넷"}
        response = requests.post(url, json=data)
        FileHandler.format_json_print(response.json())

    def test_update_translation_language(self):
        channel_id = TEST_YOUTUBE_CHANNEL_ID
        url = f"{self.base_url}channel/{channel_id}/update_translation_language"
        data = {
            "default_audio_language": "ko",
            "translation_languages": ["ja"]
        }
        response = requests.post(url, json=data)
        FileHandler.format_json_print(response.json())

    def test_get_video_data(self):
        video_id = TEST_YOUTUBE_VIDEO_ID
        url = f"{self.base_url}video/{video_id}"
        response = requests.get(url)
        FileHandler.format_json_print(response.json())

    def test_get_subtitle_text_data(self):
        subtitle_text_id = "29C698E5E667466F9BE70E47A721929E"
        url = f"{self.base_url}subtitle/{subtitle_text_id}"
        data = {
            "language_code": "ja"
        }
        response = requests.post(url, json=data)
        FileHandler.format_json_print(response.json())

    def test_update_subtitle_translation(self):
        subtitle_text_id = "29C698E5E667466F9BE70E47A721929E"
        url = f"{self.base_url}subtitle/{subtitle_text_id}/update_subtitle_translation"
        data = {
            "language_code": "ja",
            "subtitle_translation_text": "テスト",
            "subtitle_translation_text_detail": "テスト説明"
        }
        response = requests.post(url, json=data)
        FileHandler.format_json_print(response.json())

    def test_insert_or_update_subtitle_learning_memory(self):
        subtitle_text_id = "D5791D90FDA5431EAA5BE2EF0E1DB5BC"
        url = f"{self.base_url}subtitle/{subtitle_text_id}/insert_or_update_subtitle_learning_memory"
        data = {
            "language_code": "ja",
            "learning_status": 3}
        response = requests.post(url, json=data)
        FileHandler.format_json_print(response.json())

# if __name__ == '__main__':
#     unittest.main()
