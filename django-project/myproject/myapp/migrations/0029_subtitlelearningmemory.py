# Generated by Django 5.0.4 on 2024-05-24 05:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_subtitletranslation_subtitle_literal_translation_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubtitleLearningMemory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('learning_status', models.CharField(choices=[(0, 'NOT_CHECKED'), (1, 'NOT_UNDERSTOOD'), (2, 'ONE_WORD_UNKNOWN'), (3, 'FULLY_UNDERSTOOD')], verbose_name='言語コード')),
                ('last_updated', models.DateTimeField(null=True, verbose_name='最終更新日時')),
                ('subtitle_translation_text_id', models.ForeignKey(db_column='subtitle_translation_text_id', on_delete=django.db.models.deletion.CASCADE, to='myapp.subtitletranslation', verbose_name='字幕翻訳テキストID')),
            ],
            options={
                'db_table': 'subtitle_learning_memory',
                'unique_together': {('subtitle_translation_text_id', 'learning_status')},
            },
        ),
    ]