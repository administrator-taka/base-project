import logging
import unittest

from myapp.applications.domain.logic.youtube_api_logic import YouTubeApiLogic
from myapp.applications.domain.logic.youtube_subtitle_logic import YouTubeSubtitleLogic
from myapp.applications.util.code.subtitle_type import SubtitleType
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myapp.models import VideoSubtitleInfo
from myproject.settings.base import TEST_YOUTUBE_VIDEO_ID


class YoutubeDownloadService:
    def __init__(self):
        self.youtube_subtitle_logic = YouTubeSubtitleLogic()
        self.youtube_api_logic = YouTubeApiLogic()

    def download_video_subtitle(self, video_id: str,
                                default_audio_language: YouTubeLanguage,
                                translation_language: YouTubeLanguage) -> None:
        # 既に登録されているかのチェック
        existing_subtitle_info = VideoSubtitleInfo.objects.filter(
            video_id=video_id
        ).first()
        # 既に処理を行っている場合実行しない
        if not existing_subtitle_info:
            subtitle_info = self.youtube_subtitle_logic.download_subtitles_info(video_id)
            # FileHandler.write_json_response(subtitle_info)
            # subtitle_info = FileHandler.get_json_response(TEST_DIR + "test_20240427_141430.json")
            # 自動生成字幕
            self.create_or_update_video_subtitle_info(video_id, subtitle_info, SubtitleType.AUTOMATIC,
                                                      default_audio_language)
            # 手動作成字幕
            self.create_or_update_video_subtitle_info(video_id, subtitle_info, SubtitleType.MANUAL,
                                                      default_audio_language)
            self.create_or_update_video_subtitle_info(video_id, subtitle_info, SubtitleType.MANUAL,
                                                      translation_language)
        else:
            logging.debug(f"{video_id}:登録済み")

    def create_or_update_video_subtitle_info(self, video_id, subtitle_info, subtitle_type, language):
        # 既に登録されているかのチェック
        existing_subtitle_info = VideoSubtitleInfo.objects.filter(
            video_id=video_id,
            subtitle_type=subtitle_type.value,
            language_code=language.value
        ).first()

        # ビデオサブタイトル情報が存在しない場合に新しいレコードを作成
        if not existing_subtitle_info:
            # 自動生成字幕
            has_subtitle, subtitle = self.youtube_subtitle_logic.extract_and_process_subtitle(subtitle_info,
                                                                                              subtitle_type,
                                                                                              language)
            # サブタイトル情報がある場合、備考にサブタイトルを設定する
            remarks_value = subtitle if not has_subtitle else None
            VideoSubtitleInfo.objects.create(
                video_id=video_id,
                subtitle_type=subtitle_type.value,
                language_code=language.value,
                has_subtitle=has_subtitle,
                remarks=remarks_value
            )


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
