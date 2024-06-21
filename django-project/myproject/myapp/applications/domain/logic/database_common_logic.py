import datetime
import logging
import time
from datetime import datetime

from myapp.applications.util.code.subtitle_status import SubtitleStatus
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myapp.applications.util.util_generate import generate_subtitle_id, generate_uuid
from myapp.models import VideoSubtitleInfo, VideoSubtitle, VideoDetail, \
    ChannelTranslationInfo


class DatabaseCommonLogic:

    def get_translation_info(self, channel_id):
        # ChannelTranslationInfoからデータを取得
        translation_info = ChannelTranslationInfo.objects.get(channel_id=channel_id)

        if translation_info.default_audio_language is None or translation_info.translation_languages is None:
            logging.error("TODO:デフォルト言語指定エラー")
            return
        # デフォルトの言語コードを取得
        default_audio_language = YouTubeLanguage(translation_info.default_audio_language)

        # 翻訳言語リスト取得
        translation_languages = [YouTubeLanguage(language) for language in translation_info.translation_languages]

        return default_audio_language, translation_languages

    def insert_or_update_video_subtitle_info(self, video_id, subtitle_type, language, subtitle_status, last_updated):
        video_detail_instance, _ = VideoDetail.objects.get_or_create(video_id=video_id)
        subtitle_id = generate_subtitle_id(video_id, subtitle_type, language)

        # 既存のレコードがあれば取得
        video_subtitle_info = VideoSubtitleInfo.objects.filter(subtitle_id=subtitle_id).first()

        # 既存のレコードがある場合かつsubtitle_statusが1の場合は更新しない
        if video_subtitle_info and video_subtitle_info.subtitle_status == SubtitleStatus.REGISTERED.value:
            logging.debug("字幕登録済み")
        else:
            # 既存のレコードがない場合またはsubtitle_statusが1（登録済み）でない場合は新規作成または更新
            VideoSubtitleInfo.objects.update_or_create(
                subtitle_id=subtitle_id,
                defaults={
                    'video_id': video_detail_instance,
                    'subtitle_type': subtitle_type.value,
                    'language_code': language.value,
                    'subtitle_status': subtitle_status.value,
                    'last_updated': datetime.now(),
                }
            )

    def insert_subtitle_data(self, video_id, subtitle, subtitle_type, language):
        # 辞書型リストのデータを順番に処理してデータベースに挿入
        for data in subtitle:
            # 字幕情報を保存する前に、関連するVideoSubtitleInfoインスタンスを取得する必要があります
            subtitle_id = generate_subtitle_id(video_id, subtitle_type, language)
            subtitle_info_instance = VideoSubtitleInfo.objects.get(subtitle_id=subtitle_id)
            VideoSubtitle.objects.create(
                subtitle_id=subtitle_info_instance,
                subtitle_text_id=generate_uuid(),
                t_start_ms=data['t_start_ms'],
                d_duration_ms=data['d_duration_ms'],
                t_offset_ms=data['t_offset_ms'],
                subtitle_text=data['subtitle_text']
            )

    def create_or_update_video_subtitle_info(self, video_id, subtitle_info, subtitle_type, language):
        # TODO:データを用意している場合、処理が速すぎるため念のため一時停止
        time.sleep(1)
        # 自動生成字幕
        subtitle_status, subtitle = self.youtube_subtitle_logic.extract_and_process_subtitle_json(subtitle_info,
                                                                                                  subtitle_type,
                                                                                                  language)
        # 最初にインサートし、データがあればupdateするように修正
        subtitle_id = generate_subtitle_id(video_id, subtitle_type, language)

        self.insert_or_update_video_subtitle_info(video_id,
                                                  subtitle_type,
                                                  language,
                                                  SubtitleStatus.NO_SUBTITLE,
                                                  None)
        # 字幕があった場合、
        if subtitle_status == SubtitleStatus.REGISTERED:
            self.insert_subtitle_data(video_id, subtitle, subtitle_type, language)
            VideoSubtitleInfo.objects.filter(subtitle_id=subtitle_id).update(
                subtitle_status=SubtitleStatus.REGISTERED.value,
                remarks=None
            )
        # 字幕の登録に失敗した場合
        elif subtitle_status == SubtitleStatus.REGISTRATION_FAILED:
            # サブタイトル情報がある場合、備考にサブタイトルを設定する
            VideoSubtitleInfo.objects.filter(subtitle_id=subtitle_id).update(
                subtitle_status=SubtitleStatus.REGISTRATION_FAILED.value,
                remarks=subtitle
            )
