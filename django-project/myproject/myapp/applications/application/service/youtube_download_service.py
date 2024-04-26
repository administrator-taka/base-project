import logging
import unittest

from myapp.applications.domain.logic.youtube_api_logic import YouTubeApiLogic
from myapp.applications.domain.logic.youtube_subtitle_logic import YouTubeSubtitleLogic
from myapp.applications.infrastructure.repository.web_client import WebClient
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myapp.applications.util.file_handler import FileHandler
from myproject.settings.base import TEST_YOUTUBE_VIDEO_ID


class YoutubeDownloadService:
    def __init__(self):
        # APIキーをリストに登録
        self.youtube_subtitle_logic = YouTubeSubtitleLogic()
        self.youtube_api_logic = YouTubeApiLogic()

    def download_video_subtitle(self, video_id,default_audio_language=YouTubeLanguage,translation_language=YouTubeLanguage):
        subtitle_info = self.youtube_subtitle_logic.download_subtitles_info(video_id)

        # デフォルト言語:自動生成字幕
        automatic_captions = subtitle_info.get("automatic_captions")
        if automatic_captions:
            captions_info = automatic_captions.get(default_audio_language.value)
            if captions_info:
                json_data = [item for item in captions_info if item.get("ext") == "json3"]
                if json_data:
                    result_json = WebClient.make_api_request(json_data[0]["url"], None)
                    FileHandler.format_json_print(result_json)
                else:
                    logging.debug("自動生成字幕のためのJSONデータが見つかりませんでした。")
            else:
                logging.debug("自動生成字幕のデフォルト言語のキャプション情報が見つかりませんでした。")
        else:
            logging.debug("自動生成字幕が見つかりませんでした。")

        # デフォルト言語:手動作成字幕
        subtitles = subtitle_info.get("subtitles")
        if subtitles:
            captions_info = subtitles.get(default_audio_language.value)
            if captions_info:
                json_data = [item for item in captions_info if item.get("ext") == "json3"]
                if json_data:
                    result_json = WebClient.make_api_request(json_data[0]["url"], None)
                    FileHandler.format_json_print(result_json)
                else:
                    logging.debug("手動作成字幕のためのJSONデータが見つかりませんでした。")
            else:
                logging.debug("手動作成字幕のデフォルト言語のキャプション情報が見つかりませんでした。")
        else:
            logging.debug("手動作成字幕が見つかりませんでした。")

        # 翻訳言語:手動作成字幕
        if subtitles:
            captions_info = subtitles.get(translation_language.value)
            if captions_info:
                json_data = [item for item in captions_info if item.get("ext") == "json3"]
                if json_data:
                    result_json = WebClient.make_api_request(json_data[0]["url"], None)
                    FileHandler.format_json_print(result_json)
                else:
                    logging.debug("翻訳言語の手動作成字幕のためのJSONデータが見つかりませんでした。")
            else:
                logging.debug("翻訳言語の手動作成字幕のキャプション情報が見つかりませんでした。")


class TestYoutubeDownloadService(unittest.TestCase):

    def test_download_all_subtitle(self):
        youtube_download_service = YoutubeDownloadService()
        video_id = TEST_YOUTUBE_VIDEO_ID
        default_audio_language = YouTubeLanguage.KOREAN
        translation_language = YouTubeLanguage.JAPANESE

        youtube_download_service.download_video_subtitle(video_id,default_audio_language,translation_language)

# if __name__ == '__main__':
#     unittest.main()
