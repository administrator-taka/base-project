# Generated by Django 5.0.4 on 2024-05-24 03:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0027_alter_channeldetail_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtitletranslation',
            name='subtitle_literal_translation_text',
            field=models.TextField(blank=True, null=True, verbose_name='直訳翻訳'),
        ),
    ]
