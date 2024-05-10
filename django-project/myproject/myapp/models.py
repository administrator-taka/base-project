# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.postgres.fields import ArrayField
from django.db import models

from myapp.applications.util.code.subtitle_status import SubtitleStatus
from myapp.applications.util.code.subtitle_type import SubtitleType
from myapp.applications.util.code.youtube_language import YouTubeLanguage


class Test(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'test'


class ChannelDetail(models.Model):
    # チャンネルID
    channel_id = models.CharField(primary_key=True, max_length=50, verbose_name='チャンネルID')
    # チャンネルプレイリストID
    playlist_id = models.CharField(max_length=50, verbose_name='チャンネルプレイリストID')

    # チャンネルタイトル
    title = models.TextField(verbose_name='チャンネルタイトル')
    # チャンネルの説明
    description = models.TextField(verbose_name='チャンネルの説明')
    # カスタムURL
    custom_url = models.CharField(max_length=50, verbose_name='カスタムURL')
    # 公開日時
    published_at = models.DateTimeField(verbose_name='公開日時')
    # サムネイルURL
    thumbnail = models.TextField(verbose_name='サムネイルURL')
    # 国コード
    country = models.CharField(max_length=50, verbose_name='国コード')

    class Meta:
        db_table = 'channel_detail'


class ChannelTranslationInfo(models.Model):
    # チャンネルIDでChannelDetailとの関連を表現
    channel_id = models.OneToOneField(ChannelDetail, primary_key=True, db_column='channel_id', on_delete=models.CASCADE,
                                      verbose_name='チャンネルID')
    # デフォルトの言語コード（初期値はnullで後から追記する）
    default_audio_language = models.CharField(null=True, choices=[(tag.value, tag.name) for tag in YouTubeLanguage],
                                              verbose_name='デフォルトの言語コード')

    # 翻訳の言語コードリスト
    translation_languages = ArrayField(
        models.CharField(max_length=10, choices=[(tag.value, tag.name) for tag in YouTubeLanguage]),
        null=True, verbose_name='翻訳の言語コードリスト')

    class Meta:
        db_table = 'channel_translation_info'


class ChannelLocalized(models.Model):
    # チャンネルIDでChannelDetailとの関連を表現
    channel_id = models.ForeignKey(ChannelDetail, db_column='channel_id', on_delete=models.CASCADE,
                                   verbose_name='チャンネルID')
    # チャンネルタイトル
    title = models.TextField(verbose_name='チャンネルタイトル')
    # チャンネルの説明
    description = models.TextField(verbose_name='チャンネルの説明')

    class Meta:
        db_table = 'channel_localized'


class VideoDetail(models.Model):
    # チャンネルIDでChannelDetailとの関連を表現
    channel_id = models.ForeignKey(ChannelDetail, db_column='channel_id', on_delete=models.CASCADE,
                                   verbose_name='チャンネルID')
    # 動画ID
    video_id = models.CharField(primary_key=True, max_length=50, verbose_name='動画ID')

    # eタグ
    e_tag = models.CharField(max_length=50, verbose_name='eタグ')

    # 動画タイトル
    title = models.TextField(verbose_name='動画タイトル')

    # 動画の説明
    description = models.TextField(verbose_name='動画の説明')
    # 公開日時
    published_at = models.DateTimeField(verbose_name='公開日時')
    # サムネイルURL
    thumbnail = models.TextField(verbose_name='サムネイルURL')

    # デフォルトの言語コード（video リソースの snippet.title プロパティと snippet.description プロパティで指定されたテキストの言語。）
    default_language = models.CharField(null=True, choices=[(tag.value, tag.name) for tag in YouTubeLanguage],
                                        verbose_name='デフォルトのテキスト言語コード')

    # デフォルトの言語コード
    default_audio_language = models.CharField(null=True, choices=[(tag.value, tag.name) for tag in YouTubeLanguage],
                                              verbose_name='デフォルトの言語コード')

    # 配信開始日時
    actual_start_time = models.DateTimeField(null=True, verbose_name='公開日時')

    # 配信終了日時
    actual_end_time = models.DateTimeField(null=True, verbose_name='公開日時')

    # 配信予定日時
    scheduled_start_time = models.DateTimeField(null=True, verbose_name='公開日時')

    # TODO:動画の種類、動画、short、配信

    # 初期登録フラグ
    initial_flag = models.BooleanField(default=False, verbose_name='初期登録フラグ')

    # 削除フラグ
    is_disabled = models.BooleanField(default=False, verbose_name='削除フラグ')

    class Meta:
        db_table = 'video_detail'


class VideoLocalized(models.Model):
    # 動画ID
    video_id = models.ForeignKey(VideoDetail, db_column='video_id', on_delete=models.CASCADE,
                                 verbose_name='動画ID')

    # 言語コード
    language_code = models.CharField(choices=[(tag.value, tag.name) for tag in YouTubeLanguage],
                                     verbose_name='言語コード')
    # チャンネルタイトル
    channel_title = models.TextField(verbose_name='チャンネルタイトル')
    # チャンネルの説明
    description = models.TextField(verbose_name='チャンネルの説明')

    class Meta:
        db_table = 'video_localized'


class VideoSubtitleInfo(models.Model):
    # 動画ID
    video_id = models.ForeignKey(VideoDetail, db_column='video_id', on_delete=models.CASCADE,
                                 verbose_name='動画ID')
    # 字幕ID
    subtitle_id = models.CharField(primary_key=True, max_length=50, verbose_name='字幕ID')

    subtitle_type = models.IntegerField(choices=[(tag.value, tag.name) for tag in SubtitleType],
                                        verbose_name='字幕の種類')

    # 字幕の言語コード
    language_code = models.CharField(choices=[(tag.value, tag.name) for tag in YouTubeLanguage], verbose_name='言語コード')

    subtitle_status = models.IntegerField(choices=[(tag.value, tag.name) for tag in SubtitleStatus],
                                          verbose_name='字幕ステータス')

    last_updated = models.DateTimeField(verbose_name='最終更新日時', null=True)

    # 備考欄
    remarks = models.TextField(blank=True, null=True, verbose_name='備考欄')

    class Meta:
        db_table = 'video_subtitle_info'
        unique_together = ['video_id', 'subtitle_type', 'language_code']


class VideoSubtitle(models.Model):
    # 字幕IDでVideoSubtitleInfoとの関連を表現
    subtitle_id = models.ForeignKey(VideoSubtitleInfo, db_column='subtitle_id', on_delete=models.CASCADE,
                                    verbose_name='字幕ID')
    # 字幕テキストID
    subtitle_text_id = models.CharField(primary_key=True, max_length=50, verbose_name='字幕テキストID')

    # 開始時間（ミリ秒）
    t_start_ms = models.IntegerField(verbose_name='開始時間（ミリ秒）', null=True, blank=True)

    # 持続時間（ミリ秒）
    d_duration_ms = models.IntegerField(verbose_name='持続時間（ミリ秒）', null=True, blank=True)

    # オフセット時間（ミリ秒）
    t_offset_ms = models.IntegerField(verbose_name='オフセット時間（ミリ秒）', null=True, blank=True)

    # 字幕
    subtitle_text = models.TextField(blank=False, null=False, verbose_name='字幕')

    class Meta:
        db_table = 'video_subtitle'


class SubtitleTranslation(models.Model):
    # 字幕テキストID
    subtitle_text_id = models.ForeignKey(VideoSubtitle, db_column='subtitle_text_id',
                                         on_delete=models.CASCADE,
                                         verbose_name='字幕テキストID')

    # 字幕の言語コード
    language_code = models.CharField(choices=[(tag.value, tag.name) for tag in YouTubeLanguage], verbose_name='言語コード')

    # 翻訳字幕
    subtitle_transration_text = models.TextField(blank=True, null=True, verbose_name='翻訳字幕')

    # 翻訳字幕詳細
    subtitle_transration_text_detail = models.TextField(blank=True, null=True, verbose_name='翻訳字幕詳細')

    class Meta:
        db_table = 'subtitle_translation'
