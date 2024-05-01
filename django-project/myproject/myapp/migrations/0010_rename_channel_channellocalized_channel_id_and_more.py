# Generated by Django 5.0.4 on 2024-05-01 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_channellocalized_table_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='channellocalized',
            old_name='channel',
            new_name='channel_id',
        ),
        migrations.RenameField(
            model_name='subtitletranslation',
            old_name='subtitle_text',
            new_name='subtitle_text_id',
        ),
        migrations.RenameField(
            model_name='videodetail',
            old_name='channel',
            new_name='channel_id',
        ),
        migrations.RenameField(
            model_name='videolocalized',
            old_name='video',
            new_name='video_id',
        ),
        migrations.RenameField(
            model_name='videosubtitle',
            old_name='subtitle_info',
            new_name='subtitle_id',
        ),
        migrations.RenameField(
            model_name='videosubtitleinfo',
            old_name='subtitle_info_id',
            new_name='subtitle_id',
        ),
        migrations.RenameField(
            model_name='videosubtitleinfo',
            old_name='video',
            new_name='video_id',
        ),
        migrations.AlterUniqueTogether(
            name='videosubtitleinfo',
            unique_together={('video_id', 'subtitle_type', 'language_code')},
        ),
    ]
