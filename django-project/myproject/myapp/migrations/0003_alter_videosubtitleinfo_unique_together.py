# Generated by Django 5.0.4 on 2024-04-27 09:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0002_videosubtitleinfo'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='videosubtitleinfo',
            unique_together={('video_id', 'subtitle_type', 'language_code')},
        ),
    ]
