# Generated by Django 5.0.4 on 2024-05-04 17:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0018_videosubtitleinfo_last_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videosubtitleinfo',
            name='last_updated',
            field=models.DateTimeField(null=True, verbose_name='最終更新日時'),
        ),
    ]
