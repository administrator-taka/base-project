# Generated by Django 5.0.4 on 2024-05-01 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0010_rename_channel_channellocalized_channel_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channellocalized',
            name='channel_id',
            field=models.ForeignKey(db_column='channel_id', on_delete=django.db.models.deletion.CASCADE,
                                    related_name='localized_channels', to='myapp.channeldetail',
                                    verbose_name='チャンネルID'),
        ),
        migrations.AlterField(
            model_name='subtitletranslation',
            name='subtitle_text_id',
            field=models.OneToOneField(db_column='subtitle_text_id', on_delete=django.db.models.deletion.CASCADE,
                                       primary_key=True, related_name='video_subtitle', serialize=False,
                                       to='myapp.videosubtitle', verbose_name='字幕テキストID'),
        ),
        migrations.AlterField(
            model_name='videodetail',
            name='channel_id',
            field=models.ForeignKey(db_column='channel_id', on_delete=django.db.models.deletion.CASCADE,
                                    related_name='channel_detail', to='myapp.channeldetail', verbose_name='チャンネルID'),
        ),
        migrations.AlterField(
            model_name='videolocalized',
            name='video_id',
            field=models.ForeignKey(db_column='video_id', on_delete=django.db.models.deletion.CASCADE,
                                    related_name='localized_videos', to='myapp.videodetail', verbose_name='動画ID'),
        ),
        migrations.AlterField(
            model_name='videosubtitle',
            name='subtitle_id',
            field=models.ForeignKey(db_column='subtitle_id', on_delete=django.db.models.deletion.CASCADE,
                                    related_name='video_subtitle_info', to='myapp.videosubtitleinfo',
                                    verbose_name='字幕ID'),
        ),
        migrations.AlterField(
            model_name='videosubtitleinfo',
            name='video_id',
            field=models.ForeignKey(db_column='video_id', on_delete=django.db.models.deletion.CASCADE,
                                    related_name='video_detail', to='myapp.videodetail', verbose_name='動画ID'),
        ),
    ]
