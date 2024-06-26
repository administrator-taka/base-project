# Generated by Django 5.0.4 on 2024-05-01 07:23

import datetime

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0004_alter_videosubtitledetail_subtitle_transration_text_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videosubtitledetail',
            name='subtitle_text',
        ),
        migrations.AddField(
            model_name='videosubtitledetail',
            name='subtitle_text_id',
            field=models.OneToOneField(
                default=datetime.datetime(2024, 5, 1, 7, 23, 24, 776183, tzinfo=datetime.timezone.utc),
                on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='subtitle', serialize=False,
                to='myapp.videosubtitle', verbose_name='字幕テキストID'),
            preserve_default=False,
        ),
    ]
