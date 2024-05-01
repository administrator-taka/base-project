import logging
import unittest
from typing import List

from myapp.applications.domain.logic.youtube_api_logic import YouTubeApiLogic
from myapp.applications.domain.logic.youtube_subtitle_logic import YouTubeSubtitleLogic
from myapp.applications.util.code.subtitle_type import SubtitleType
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myapp.applications.util.util_generate import generate_subtitle_id, generate_uuid
from myapp.models import VideoSubtitleInfo, VideoSubtitle, SubtitleTranslation, ChannelDetail, VideoDetail, \
    ChannelTranslationInfo
from myproject.settings.base import TEST_YOUTUBE_VIDEO_ID, TEST_YOUTUBE_PLAYLIST_ID
from collections import defaultdict


class YoutubeDownloadService:
    def __init__(self):
        self.youtube_subtitle_logic = YouTubeSubtitleLogic()
        self.youtube_api_logic = YouTubeApiLogic()

    def insert_initial_channel_data(self, channel_id):
        # チャンネルIDに紐づくチャンネル情報を取得
        channel_data = ChannelDetail.objects.filter(
            channel_id=channel_id
        ).first()
        channel_playlist_id = None;
        # チャンネル情報が存在しない場合は追加
        if not channel_data:
            channel_data = self.youtube_api_logic.get_channel_details_data(channel_id)
            if channel_data:
                # 新しいチャンネルデータを作成して保存
                new_channel = ChannelDetail.objects.create(
                    channel_id=channel_data['channel_id'],
                    playlist_id=channel_data['playlist_id'],
                    title=channel_data['title'],
                    description=channel_data['description'],
                    custom_url=channel_data['custom_url'],
                    published_at=channel_data['published_at'],
                    thumbnail=channel_data['thumbnail'],
                    country=channel_data['country']
                )
                channel_playlist_id = channel_data['playlist_id']
                ChannelTranslationInfo.objects.create(
                    channel_id=new_channel,
                    default_audio_language=None,
                    translation_languages=None
                )
                logging.debug("チャンネル情報が追加されました。")

            else:
                logging.debug("チャンネル情報が見つかりませんでした。")
        else:
            logging.debug("チャンネル情報は既に存在します。")
            channel_playlist_id = channel_data.playlist_id

        playlist_videos = self.youtube_api_logic.get_channel_videos(channel_playlist_id)
        for video_data in playlist_videos:
            self.insert_or_update_video_detail(video_data)

    def insert_or_update_video_detail(self, video_data):
        video_id = video_data['video_id']
        e_tag = video_data['e_tag']
        title = video_data['title']
        published_at = video_data['published_at']
        description = video_data['description']
        thumbnail = video_data['thumbnail']
        channel_id = video_data['channel_id']

        # video_idで既存のレコードを取得する
        try:
            video_detail = VideoDetail.objects.get(video_id=video_id)
        except VideoDetail.DoesNotExist:
            # 既存のレコードがない場合は新規作成
            VideoDetail.objects.create(
                video_id=video_id,
                e_tag=e_tag,
                title=title,
                published_at=published_at,
                description=description,
                thumbnail=thumbnail,
                channel_id=ChannelDetail.objects.get(channel_id=channel_id),
            )
            logging.debug("動画情報が追加されました。")
            return

        # 既存のレコードがある場合、etagが異なる場合のみ更新
        if video_detail.e_tag != e_tag:
            video_detail.title = title
            video_detail.published_at = published_at
            video_detail.description = description
            video_detail.thumbnail = thumbnail
            video_detail.channel_id = ChannelDetail.objects.get(channel_id=channel_id)
            video_detail.e_tag = e_tag
            video_detail.save()
            logging.debug("動画情報が更新されました。")
        else:
            logging.debug("動画情報は既に最新です。")

    def get_channel_subtitle_list(self, channel_id):
        # Django ORMを使用してクエリを構築
        queryset = VideoSubtitleInfo.objects.filter(
            subtitle_type=SubtitleType.MANUAL.value,
        )

        # video_idごとに字幕情報をまとめるための辞書を作成
        subtitle_info_by_video = defaultdict(list)
        for info in queryset:
            subtitle_info_by_video[info.video_id].append(info)

        # 辞書の内容を表示
        for video_id, infos in subtitle_info_by_video.items():
            print("Video ID:", video_id)
            for info in infos:
                print(info.language_code, info.has_subtitle)

    def insert_initial_subtitle_detail(self, video_id):
        # Django ORMを使用してクエリを構築
        queryset = VideoSubtitle.objects.filter(
            subtitle_info__subtitle_type=SubtitleType.MANUAL.value,
            subtitle_info__video_id=video_id
        )

        # 韓国語字幕のクエリ
        ko_queryset = queryset.filter(subtitle_info__language_code=YouTubeLanguage.KOREAN.value)

        # 日本語字幕のクエリ
        ja_queryset = queryset.filter(subtitle_info__language_code=YouTubeLanguage.JAPANESE.value)

        # クエリセットを実行
        ko_results = list(ko_queryset.order_by('t_start_ms'))
        ja_results = list(ja_queryset.order_by('t_start_ms'))

        if self.check_subtitle_text_id_exists(
                generate_subtitle_id(video_id, SubtitleType.MANUAL, YouTubeLanguage.KOREAN)):
            logging.debug('既にある')
            return

        if len(ko_results) == len(ja_results):
            for ko_result, ja_result in zip(ko_results, ja_results):
                if ko_result.t_start_ms == ja_result.t_start_ms:
                    # VideoSubtitle のインスタンスを取得
                    subtitle_instance = VideoSubtitle.objects.get(subtitle_text_id=ko_result.subtitle_text_id)

                    # VideoSubtitleDetail のインスタンスを作成し、subtitle_text_id に subtitle_instance を割り当てる
                    SubtitleTranslation.objects.create(
                        subtitle_text_id=subtitle_instance,
                        subtitle_transration_text=ja_result.subtitle_text,
                        subtitle_transration_text_detail=None,
                    )
                    print(ko_result.subtitle_text_id, ko_result.subtitle_text, ja_result.subtitle_text)
        else:
            logging.debug('一致する字幕情報なし')

    def check_subtitle_text_id_exists(self, subtitle_id):
        # 特定の subtitle_id に対応する VideoSubtitleDetail レコードが存在するかチェック
        exists = SubtitleTranslation.objects.filter(subtitle_text_id__subtitle_info__subtitle_id=subtitle_id).exists()
        return exists

    def download_channel_subtitles(self, channel_id: str) -> None:
        self.insert_initial_channel_data(channel_id)
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

        # TODO:リストが単体だと動作不良を起こすため明示的に彩度リストに格納
        if not isinstance(translation_languages, list):
            translation_languages = [translation_languages]

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
            # 最初にインサートし、データがあればupdateするように修正
            subtitle_id = generate_subtitle_id(video_id, subtitle_type, language)
            VideoSubtitleInfo.objects.create(
                subtitle_id=subtitle_id,
                video_id=video_id,
                subtitle_type=subtitle_type.value,
                language_code=language.value,
                has_subtitle=has_subtitle,
                remarks=None
            )
            if has_subtitle:
                self.insert_subtitle_data(video_id, subtitle, subtitle_type, language)
            # サブタイトル情報がある場合、備考にサブタイトルを設定する
            remarks_value = subtitle if not has_subtitle else None
            VideoSubtitleInfo.objects.filter(subtitle_id=subtitle_id).update(
                has_subtitle=True,
                remarks=remarks_value
            )

    def insert_subtitle_data(self, video_id, subtitle, subtitle_type, language):
        # 辞書型リストのデータを順番に処理してデータベースに挿入
        for data in subtitle:
            VideoSubtitle.objects.create(
                subtitle_text_id=generate_uuid(),
                subtitle_info_id=generate_subtitle_id(video_id, subtitle_type, language),
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
