# Generated by Django 5.0.4 on 2024-05-01 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_rename_videosubtitledetail_subtitletranslation_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='channellocalized',
            table='channel_localized',
        ),
        migrations.AlterModelTable(
            name='videolocalized',
            table='video_localized',
        ),
    ]
