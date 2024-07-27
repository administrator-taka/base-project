import unittest

import requests

from myapp.applications.util.file_handler import FileHandler
from myproject.settings.base import TEST_YOUTUBE_CHANNEL_ID, TEST_YOUTUBE_VIDEO_ID


class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/youtube_app/"

    def test_get_channel_list(self):
        url = f"{self.base_url}channel"
        response = requests.get(url)
        FileHandler.format_json_print(response.json())

    def test_get_channel_data(self):
        channel_id = TEST_YOUTUBE_CHANNEL_ID
        url = f"{self.base_url}channel/{channel_id}"
        response = requests.get(url)
        FileHandler.format_json_print(response.json())

    def test_calculate_channel_word(self):
        channel_id = TEST_YOUTUBE_CHANNEL_ID
        url = f"{self.base_url}channel/{channel_id}/calculate_channel_word"
        data = {
            'min_word': 3,
            'min_word_length': 2,
            'top_n': 100,
            'subtitle_type': 1,
            'stop_word_flag': False,
            'lemmatize_flag': True
        }
        response = requests.post(url, json=data)
        FileHandler.format_json_print(response.json())

    def test_get_channel_video_list(self):
        channel_id = TEST_YOUTUBE_CHANNEL_ID
        url = f"{self.base_url}channel/{channel_id}/get_channel_video_list"
        data = {
            'page': 1,
            'page_size': 10,
            'languages': ["ja"]
        }
        response = requests.post(url, json=data)
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

    def test_search_multiple_word(self):
        channel_id = TEST_YOUTUBE_CHANNEL_ID
        url = f"{self.base_url}channel/{channel_id}/search_multiple_word"
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

    def test_update_channel_subtitles(self):
        channel_id = TEST_YOUTUBE_CHANNEL_ID
        url = f"{self.base_url}channel/{channel_id}/update_channel_subtitles"
        response = requests.get(url)
        FileHandler.format_json_print(response.json())

    def test_get_video_data(self):
        video_id = TEST_YOUTUBE_VIDEO_ID
        url = f"{self.base_url}video/{video_id}"
        response = requests.get(url)
        FileHandler.format_json_print(response.json())

    def test_download_video_subtitle(self):
        video_id = TEST_YOUTUBE_VIDEO_ID
        url = f"{self.base_url}video/{video_id}/download_video_subtitle"
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

    def test_execute_chatgpt_translation(self):
        subtitle_text_id = "D5791D90FDA5431EAA5BE2EF0E1DB5BC"
        url = f"{self.base_url}subtitle/{subtitle_text_id}/execute_chatgpt_translation"
        data = {
            "language_code": "ja",
            "call_api": False,
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
            "favorite": True,
            "learning_status": 3}
        response = requests.post(url, json=data)
        FileHandler.format_json_print(response.json())

    def test_get_learning_subtitle_text_list(self):
        url = f"{self.base_url}learning"
        data = {
            "language_code": "ko",
            "learning_status": 3}
        response = requests.post(url, json=data)
        FileHandler.format_json_print(response.json())

    def test_get_favorite_subtitle_text_list(self):
        url = f"{self.base_url}favorite"
        data = {
            "language_code": "ko"}
        response = requests.post(url, json=data)
        FileHandler.format_json_print(response.json())

    def test_create_base_language(self):
        url = f"{self.base_url}base-language/create"
        data = {
            "language_code": "en",
            "documents": "Sample documents",
            "is_published": True,
            "learning_language_documents": "Sample learning language documents",
            "learning_language_explanation": "Sample explanation",
            "learning_language_video_id": "sample_video_id",
            "learning_language_timestamp_ms": 123456
        }
        response = requests.post(url, json=data)
        print(response.json())  # もしくは適切なフォーマット関数を使ってください

    def test_get_base_language_list(self):
        url = f"{self.base_url}base-language/list"
        response = requests.get(url)
        print(response.json())  # もしくは適切なフォーマット関数を使ってください

    def test_get_base_language_detail(self):
        base_language_id = "e2ad8ca2-2164-47c6-a134-d78d946b78d4"  # 取得したいベース言語IDに置き換えてください
        url = f"{self.base_url}base-language/{base_language_id}/detail"
        response = requests.get(url)
        print(response.json())  # もしくは適切なフォーマット関数を使ってください

    def test_update_base_language(self):
        base_language_id = "e2ad8ca2-2164-47c6-a134-d78d946b78d4"  # 更新したいベース言語IDに置き換えてください
        url = f"{self.base_url}base-language/{base_language_id}/update"
        data = {
            "documents": "Updated documents",
            "is_published": False
        }
        response = requests.put(url, json=data)
        print(response.json())  # もしくは適切なフォーマット関数を使ってください

    def test_delete_base_language(self):
        base_language_id = "e2ad8ca2-2164-47c6-a134-d78d946b78d4"  # 削除したいベース言語IDに置き換えてください
        url = f"{self.base_url}base-language/{base_language_id}/delete"
        response = requests.delete(url)
        print(response.json())  # もしくは適切なフォーマット関数を使ってください

    def test_create_learning_language(self):
        url = f"{self.base_url}learning-language/create"
        data = {
            "base_language_id": "e2ad8ca2-2164-47c6-a134-d78d946b78d4",  # 作成するベース言語IDに置き換えてください
            "language_code": "es",
            "documents": "Learning documents",
            "explanation": "Learning explanation",
            "video_id": "sample_video_id",
            "timestamp_ms": 123456
        }
        response = requests.post(url, json=data)
        print(response.json())  # もしくは適切なフォーマット関数を使ってください

    def test_get_learning_language_detail(self):
        learning_language_id = "289d3942-3a9d-4af1-8924-c1b3ce229f6e"  # 取得したい学習言語IDに置き換えてください
        url = f"{self.base_url}learning-language/{learning_language_id}/detail"
        response = requests.get(url)
        print(response.json())  # もしくは適切なフォーマット関数を使ってください

    def test_update_learning_language(self):
        learning_language_id = "289d3942-3a9d-4af1-8924-c1b3ce229f6e"  # 更新したい学習言語IDに置き換えてください
        url = f"{self.base_url}learning-language/{learning_language_id}/update"
        data = {
            "documents": "Updated learning documents",
            "explanation": "Updated explanation",
            "video_id": "updated_video_id",
            "timestamp_ms": 654321
        }
        response = requests.put(url, json=data)
        print(response.json())  # もしくは適切なフォーマット関数を使ってください

    def test_delete_learning_language(self):
        learning_language_id = "289d3942-3a9d-4af1-8924-c1b3ce229f6e"  # 削除したい学習言語IDに置き換えてください
        url = f"{self.base_url}learning-language/{learning_language_id}/delete"
        response = requests.delete(url)
        print(response.json())  # もしくは適切なフォーマット関数を使ってください

# if __name__ == '__main__':
#     unittest.main()
