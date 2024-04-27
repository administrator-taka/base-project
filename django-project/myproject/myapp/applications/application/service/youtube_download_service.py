import logging
import unittest

from django.conf import settings

from myapp.applications.domain.logic.youtube_api_logic import YouTubeApiLogic
from myapp.applications.domain.logic.youtube_subtitle_logic import YouTubeSubtitleLogic
from myapp.applications.infrastructure.repository.web_client import WebClient
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myapp.applications.util.file_handler import FileHandler
from myproject.settings.base import TEST_YOUTUBE_VIDEO_ID


class YoutubeDownloadService:
    def __init__(self):
        self.youtube_subtitle_logic = YouTubeSubtitleLogic()
        self.youtube_api_logic = YouTubeApiLogic()

    def download_video_subtitle(self, video_id: str,
                                default_audio_language: YouTubeLanguage,
                                translation_language: YouTubeLanguage) -> None:
        subtitle_info = self.youtube_subtitle_logic.download_subtitles_info(video_id)

        self.extract_and_process_subtitle(subtitle_info, "automatic_captions", default_audio_language)
        self.extract_and_process_subtitle(subtitle_info, "subtitles", default_audio_language)
        self.extract_and_process_subtitle(subtitle_info, "subtitles", translation_language)

    def extract_and_process_subtitle(self, subtitle_info, subtitle_type, language):
        # デフォルト言語:手動作成字幕
        subtitles = subtitle_info.get(subtitle_type)
        # 翻訳言語:手動作成字幕
        if subtitles:
            captions_info = subtitles.get(language.value)
            if captions_info:
                json_data = [item for item in captions_info if item.get("ext") == "json3"]
                if json_data:
                    result_json = WebClient.make_api_request(json_data[0]["url"], None)
                    FileHandler.write_json_response(result_json)
                    # result_json = process_result(result_json)
                    # FileHandler.format_json_print(result_json)
                else:
                    logging.debug("字幕のためのJSONデータが見つかりませんでした。")
            else:
                logging.debug("字幕のキャプション情報が見つかりませんでした。")
        else:
            logging.debug("字幕が見つかりませんでした。")


class TestYoutubeDownloadService(unittest.TestCase):
    def setUp(self):
        # テスト前の準備
        self.youtube_download_service = YoutubeDownloadService()
        settings.configure()

    def test_download_video_subtitle(self):
        video_id = TEST_YOUTUBE_VIDEO_ID
        default_audio_language = YouTubeLanguage.JAPANESE
        translation_language = YouTubeLanguage.JAPANESE

        self.youtube_download_service.download_video_subtitle(video_id, default_audio_language, translation_language)

# if __name__ == '__main__':
#     unittest.main()
