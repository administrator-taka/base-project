# Generated by Django 5.0.4 on 2024-07-05 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0033_subtitlelearningmemory_favorite'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('user_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('user_name', models.CharField(blank=True, max_length=50, null=True)),
                ('password', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'user_data',
            },
        ),
    ]
