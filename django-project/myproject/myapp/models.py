# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Test(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'test'


class VideoSubtitleInfo(models.Model):
    # 動画ID
    video_id = models.CharField(max_length=50, verbose_name='動画ID')

    # 字幕の種類 (自動/手動)
    subtitle_type = models.CharField(max_length=10, verbose_name='自動/手動')

    # 字幕の言語コード
    language_code = models.CharField(max_length=10, verbose_name='言語コード')

    # 字幕の有無 (True: 字幕あり, False: 字幕なし)
    has_subtitle = models.BooleanField(verbose_name='字幕があるかないか')

    # 備考欄
    remarks = models.TextField(blank=True, null=True, verbose_name='備考欄')

    class Meta:
        db_table = 'video_subtitle_info'
        unique_together = ['video_id', 'subtitle_type', 'language_code']
