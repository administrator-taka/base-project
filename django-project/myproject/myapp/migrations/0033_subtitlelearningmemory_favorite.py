# Generated by Django 5.0.4 on 2024-06-16 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0032_alter_channeltranslationinfo_default_audio_language_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtitlelearningmemory',
            name='favorite',
            field=models.BooleanField(default=False, verbose_name='お気に入り'),
        ),
    ]