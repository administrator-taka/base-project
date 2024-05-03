# Generated by Django 5.0.4 on 2024-05-01 11:40

import django.db.models.deletion
from django.db import migrations, models
from datetime import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_rename_subtitle_id_videosubtitleinfo_subtitle_info_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VideoSubtitleDetail',
            new_name='SubtitleTranslation',
        ),
        migrations.RenameField(
            model_name='channeldetail',
            old_name='channel_playlist_id',
            new_name='playlist_id',
        ),
        migrations.AddField(
            model_name='channeldetail',
            name='country',
            field=models.CharField(default=1, max_length=50, verbose_name='国コード'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channeldetail',
            name='custom_url',
            field=models.CharField(default=1, max_length=50, verbose_name='カスタムURL'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channeldetail',
            name='description',
            field=models.TextField(default=1, verbose_name='チャンネルの説明'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channeldetail',
            name='published_at',
            field=models.DateTimeField(default=datetime.now(), verbose_name='公開日時'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channeldetail',
            name='thumbnail',
            field=models.TextField(default=1, verbose_name='サムネイルURL'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channeldetail',
            name='title',
            field=models.TextField(default=1, verbose_name='チャンネルタイトル'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videodetail',
            name='actual_end_time',
            field=models.DateTimeField(null=True, verbose_name='公開日時'),
        ),
        migrations.AddField(
            model_name='videodetail',
            name='actual_start_time',
            field=models.DateTimeField(null=True, verbose_name='公開日時'),
        ),
        migrations.AddField(
            model_name='videodetail',
            name='default_audio_language',
            field=models.CharField(choices=[('ja', 'JAPANESE'), ('en', 'ENGLISH'), ('ko', 'KOREAN'), ('zh', 'CHINESE'), ('id', 'INDONESIAN')], null=True, verbose_name='デフォルトの言語コード'),
        ),
        migrations.AddField(
            model_name='videodetail',
            name='default_language',
            field=models.CharField(choices=[('ja', 'JAPANESE'), ('en', 'ENGLISH'), ('ko', 'KOREAN'), ('zh', 'CHINESE'), ('id', 'INDONESIAN')], null=True, verbose_name='デフォルトのテキスト言語コード'),
        ),
        migrations.AddField(
            model_name='videodetail',
            name='description',
            field=models.TextField(default=1, verbose_name='動画の説明'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videodetail',
            name='e_tag',
            field=models.CharField(default=1, max_length=50, verbose_name='eタグ'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videodetail',
            name='published_at',
            field=models.DateTimeField(default=datetime.now(), verbose_name='公開日時'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videodetail',
            name='scheduled_start_time',
            field=models.DateTimeField(null=True, verbose_name='公開日時'),
        ),
        migrations.AddField(
            model_name='videodetail',
            name='thumbnail',
            field=models.TextField(default=1, verbose_name='サムネイルURL'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videodetail',
            name='title',
            field=models.TextField(default=1, verbose_name='動画タイトル'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='channeldetail',
            name='default_audio_language',
            field=models.CharField(choices=[('ja', 'JAPANESE'), ('en', 'ENGLISH'), ('ko', 'KOREAN'), ('zh', 'CHINESE'), ('id', 'INDONESIAN')], null=True, verbose_name='デフォルトの言語コード'),
        ),
        migrations.AlterField(
            model_name='videosubtitleinfo',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_detail', to='myapp.videodetail', verbose_name='動画ID'),
        ),
        migrations.CreateModel(
            name='ChannelLocalized',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='チャンネルタイトル')),
                ('description', models.TextField(verbose_name='チャンネルの説明')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='localized_channels', to='myapp.channeldetail', verbose_name='チャンネルID')),
            ],
        ),
        migrations.CreateModel(
            name='VideoLocalized',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(choices=[('ja', 'JAPANESE'), ('en', 'ENGLISH'), ('ko', 'KOREAN'), ('zh', 'CHINESE'), ('id', 'INDONESIAN')], verbose_name='言語コード')),
                ('channel_title', models.TextField(verbose_name='チャンネルタイトル')),
                ('description', models.TextField(verbose_name='チャンネルの説明')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='localized_videos', to='myapp.videodetail', verbose_name='動画ID')),
            ],
        ),
    ]