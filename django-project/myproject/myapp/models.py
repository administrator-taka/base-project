# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from myapp.applications.util.code.subtitle_type import SubtitleType
from myapp.applications.util.code.youtube_language import YouTubeLanguage


class Test(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'test'


class VideoSubtitleInfo(models.Model):
    # 字幕ID
    subtitle_id = models.CharField(primary_key=True, max_length=50, verbose_name='字幕ID')

    # 動画ID
    video_id = models.CharField(max_length=50, verbose_name='動画ID')

    subtitle_type = models.IntegerField(choices=[(tag.value, tag.name) for tag in SubtitleType],
                                        verbose_name='字幕の種類')

    # 字幕の言語コード
    language_code = models.CharField(choices=[(tag.value, tag.name) for tag in YouTubeLanguage], verbose_name='言語コード')

    # 字幕の有無 (True: 字幕あり, False: 字幕なし)
    has_subtitle = models.BooleanField(verbose_name='字幕があるかないか')

    # 備考欄
    remarks = models.TextField(blank=True, null=True, verbose_name='備考欄')

    class Meta:
        db_table = 'video_subtitle_info'
        unique_together = ['video_id', 'subtitle_type', 'language_code']


class VideoSubtitle(models.Model):
    # 字幕テキストID
    subtitle_text_id = models.CharField(primary_key=True, max_length=50, verbose_name='字幕テキストID')

    # 字幕IDでVideoSubtitleInfoとの関連を表現
    subtitle_info = models.ForeignKey(VideoSubtitleInfo, on_delete=models.CASCADE, related_name='subtitles',
                                      verbose_name='字幕ID')
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


class VideoSubtitleDetail(models.Model):
    # 字幕テキストID
    subtitle_text_id = models.OneToOneField(VideoSubtitle, primary_key=True, on_delete=models.CASCADE, related_name='subtitle', verbose_name='字幕テキストID')

    # 翻訳字幕
    subtitle_transration_text = models.TextField(blank=True, null=True, verbose_name='翻訳字幕')

    # 翻訳字幕詳細
    subtitle_transration_text_detail = models.TextField(blank=True, null=True, verbose_name='翻訳字幕詳細')

    class Meta:
        db_table = 'video_subtitle_detail'
