import logging
import unittest

from django.conf import settings

from myapp.applications.domain.logic.youtube_api_logic import YouTubeApiLogic
from myapp.applications.domain.logic.youtube_subtitle_logic import YouTubeSubtitleLogic
from myapp.applications.infrastructure.repository.web_client import WebClient
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
        self.extract_and_process_subtitle(subtitle_info, "automatic_captions", default_audio_language)
        # 手動作成字幕
        self.extract_and_process_subtitle(subtitle_info, "subtitles", default_audio_language)
        self.extract_and_process_subtitle(subtitle_info, "subtitles", translation_language)

    # 字幕詳細からjsonのurlを取得
    def extract_and_process_subtitle(self, subtitle_info, subtitle_type, language):
        subtitles = subtitle_info.get(subtitle_type)
        if subtitles:
            captions_info = subtitles.get(language.value)
            if captions_info:
                json_data = [item for item in captions_info if item.get("ext") == "json3"]
                if json_data:
                    url = json_data[0]["url"]
                    self.format_subtitle(url)
                else:
                    logging.debug("字幕のためのJSONデータが見つかりませんでした。")
            else:
                logging.debug("字幕のキャプション情報が見つかりませんでした。")
        else:
            logging.debug("字幕が見つかりませんでした。")

    def format_subtitle(self, url):
        result_json = WebClient.make_api_request(url, None)
        events = result_json.get("events")
        for event in events:
            # 開始時間
            t_start_ms = event.get("tStartMs")
            # 持続時間
            d_duration_ms = event.get("dDurationMs")
            segs = event.get("segs")
            if segs:
                if len(segs) == 1:
                    print("この下★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")
                    print(segs[0].get("utf8"))
                    print("★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")
                else:
                    print("複数ある！！！")
                    for seg in segs:
                        t_offset_ms = seg.get("tOffsetMs")
                        text = seg.get("utf8")
                        print(t_offset_ms, text)
            # print(t_start_ms,d_duration_ms,segs)

        # result=segs
        # FileHandler.write_json_response(result)
        # FileHandler.format_json_print(result)


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
