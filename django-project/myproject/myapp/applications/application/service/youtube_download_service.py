import unittest

from django.conf import settings

from myapp.applications.domain.logic.youtube_api_logic import YouTubeApiLogic
from myapp.applications.domain.logic.youtube_subtitle_logic import YouTubeSubtitleLogic
from myapp.applications.util.code.subtitle_type import SubtitleType
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myapp.applications.util.file_handler import FileHandler
from myproject.settings.base import TEST_YOUTUBE_VIDEO_ID, TEST_DIR


class YoutubeDownloadService:
    def __init__(self):
        self.youtube_subtitle_logic = YouTubeSubtitleLogic()
        self.youtube_api_logic = YouTubeApiLogic()

    def download_video_subtitle(self, video_id: str,
                                default_audio_language: YouTubeLanguage,
                                translation_language: YouTubeLanguage) -> None:
        # subtitle_info = self.youtube_subtitle_logic.download_subtitles_info(video_id)
        # FileHandler.write_json_response(subtitle_info)
        subtitle_info = FileHandler.get_json_response(TEST_DIR + "test_20240427_141430.json")

        # 自動生成字幕
        self.youtube_subtitle_logic.extract_and_process_subtitle(subtitle_info, SubtitleType.AUTOMATIC,
                                                                 default_audio_language)
        # 手動作成字幕
        self.youtube_subtitle_logic.extract_and_process_subtitle(subtitle_info, SubtitleType.MANUAL,
                                                                 default_audio_language)
        self.youtube_subtitle_logic.extract_and_process_subtitle(subtitle_info, SubtitleType.MANUAL,
                                                                 translation_language)


class TestYoutubeDownloadService(unittest.TestCase):
    def setUp(self):
        # テスト前の準備
        self.youtube_download_service = YoutubeDownloadService()
        settings.configure()

    def test_download_video_subtitle(self):
        video_id = TEST_YOUTUBE_VIDEO_ID
        default_audio_language = YouTubeLanguage.KOREAN
        translation_language = YouTubeLanguage.JAPANESE

        self.youtube_download_service.download_video_subtitle(video_id, default_audio_language, translation_language)

# if __name__ == '__main__':
#     unittest.main()
