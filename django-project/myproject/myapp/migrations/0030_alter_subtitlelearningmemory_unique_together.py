# Generated by Django 5.0.4 on 2024-05-24 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0029_subtitlelearningmemory'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subtitlelearningmemory',
            unique_together={('subtitle_translation_text_id',)},
        ),
    ]
