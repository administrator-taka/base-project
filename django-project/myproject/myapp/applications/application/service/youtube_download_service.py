import logging
import unittest
from typing import List

from myapp.applications.domain.logic.youtube_api_logic import YouTubeApiLogic
from myapp.applications.domain.logic.youtube_subtitle_logic import YouTubeSubtitleLogic
from myapp.applications.util.code.subtitle_type import SubtitleType
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myapp.applications.util.util_generate import generate_subtitle_id, generate_uuid
from myapp.models import VideoSubtitleInfo, VideoSubtitle
from myproject.settings.base import TEST_YOUTUBE_VIDEO_ID, TEST_YOUTUBE_PLAYLIST_ID


class YoutubeDownloadService:
    def __init__(self):
        self.youtube_subtitle_logic = YouTubeSubtitleLogic()
        self.youtube_api_logic = YouTubeApiLogic()

    def download_channel_subtitles(self, channel_id: str) -> None:
        default_audio_language = YouTubeLanguage.KOREAN
        translation_languages = [YouTubeLanguage.JAPANESE]

        # playlist_id = self.youtube_api_logic.get_channel_id_playlist_id(channel_id)
        playlist_id = TEST_YOUTUBE_PLAYLIST_ID
        playlist_videos = self.youtube_api_logic.get_channel_videos(playlist_id)

        for video in playlist_videos:
            video_id = video.get("video_id")
            # 字幕IDが存在するかのチェックを行うデータ準備
            subtitle_ids = [generate_subtitle_id(video_id, SubtitleType.AUTOMATIC, default_audio_language)]
            for language in translation_languages:
                subtitle_ids.append(generate_subtitle_id(video_id, SubtitleType.MANUAL, language))
            # 既に登録されているかのチェック
            existing_subtitle_info = self.check_subtitle_existence(video_id, subtitle_ids)

            # 既に処理を行っている場合実行しない
            if not existing_subtitle_info:
                self.download_video_subtitle(video_id, default_audio_language, translation_languages)
            else:
                logging.debug(f"{video_id}:登録済み")

    def check_subtitle_existence(self, video_id, subtitle_ids):
        """
        指定された video_id と複数の subtitle_ids を持つサブタイトルがすべて存在するかどうかを確認します。

        :param video_id: ビデオのID
        :param subtitle_ids: 確認したいサブタイトルのIDのリスト
        :return: すべてのサブタイトルが存在する場合は True、少なくとも1つでも存在しない場合は False
        """
        # ビデオIDに基づいてすべてのサブタイトル情報を取得します
        existing_subtitle_info = VideoSubtitleInfo.objects.filter(
            video_id=video_id
        )

        # 各 subtitle_id をチェックします
        for subtitle_id in subtitle_ids:
            # 指定された subtitle_id を持つレコードが存在するかどうかを確認します
            subtitle_exists = any(subtitle_info.subtitle_id == subtitle_id for subtitle_info in existing_subtitle_info)

            # もし存在しない subtitle_id が見つかれば False を返します
            if not subtitle_exists:
                return False

        # すべての subtitle_id が見つかった場合に True を返します
        return True

    def download_video_subtitle(self, video_id: str,
                                default_audio_language: YouTubeLanguage,
                                translation_languages: List[YouTubeLanguage]) -> None:

        subtitle_info = self.youtube_subtitle_logic.download_subtitles_info(video_id)
        # FileHandler.write_json_response(subtitle_info)
        # subtitle_info = FileHandler.get_json_response(TEST_DIR + "test_20240427_141430.json")
        # 自動生成字幕
        self.create_or_update_video_subtitle_info(video_id, subtitle_info, SubtitleType.AUTOMATIC,
                                                  default_audio_language)
        # 手動作成字幕
        self.create_or_update_video_subtitle_info(video_id, subtitle_info, SubtitleType.MANUAL,
                                                  default_audio_language)
        for language in translation_languages:
            self.create_or_update_video_subtitle_info(video_id, subtitle_info, SubtitleType.MANUAL,
                                                      language)

    def create_or_update_video_subtitle_info(self, video_id, subtitle_info, subtitle_type, language):
        # 既に登録されているかのチェック
        existing_subtitle_info = VideoSubtitleInfo.objects.filter(
            subtitle_id=generate_subtitle_id(video_id, subtitle_type, language),
        ).first()

        # ビデオサブタイトル情報が存在しない場合に新しいレコードを作成
        if not existing_subtitle_info:
            # 自動生成字幕
            has_subtitle, subtitle = self.youtube_subtitle_logic.extract_and_process_subtitle_json(subtitle_info,
                                                                                                   subtitle_type,
                                                                                                   language)
            if has_subtitle:
                self.insert_subtitle_data(video_id, subtitle, subtitle_type, language)
            # サブタイトル情報がある場合、備考にサブタイトルを設定する
            remarks_value = subtitle if not has_subtitle else None
            VideoSubtitleInfo.objects.create(
                subtitle_id=generate_subtitle_id(video_id, subtitle_type, language),
                video_id=video_id,
                subtitle_type=subtitle_type.value,
                language_code=language.value,
                has_subtitle=has_subtitle,
                remarks=remarks_value
            )

    def insert_subtitle_data(self, video_id, subtitle, subtitle_type, language):
        # 辞書型リストのデータを順番に処理してデータベースに挿入
        for data in subtitle:
            VideoSubtitle.objects.create(
                subtitle_text_id=generate_uuid(),
                subtitle_id=generate_subtitle_id(video_id, subtitle_type, language),
                t_start_ms=data['t_start_ms'],
                d_duration_ms=data['d_duration_ms'],
                t_offset_ms=data['t_offset_ms'],
                subtitle_text=data['subtitle_text']
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
