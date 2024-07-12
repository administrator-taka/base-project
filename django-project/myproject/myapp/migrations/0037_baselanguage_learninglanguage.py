# Generated by Django 5.0.4 on 2024-07-12 07:40

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0036_alter_subtitlelearningmemory_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseLanguage',
            fields=[
                ('base_language_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ベース言語ID')),
                ('language_code', models.CharField(choices=[('ja', 'JAPANESE'), ('en', 'ENGLISH'), ('ko', 'KOREAN'), ('zh', 'CHINESE'), ('id', 'INDONESIAN'), ('af', 'AFRIKAANS'), ('am', 'AMHARIC'), ('ar', 'ARABIC'), ('as', 'ASSAMESE'), ('az', 'AZERBAIJANI'), ('be', 'BELARUSIAN'), ('bn', 'BENGALI'), ('bs', 'BOSNIAN'), ('ca', 'CATALAN'), ('cs', 'CZECH'), ('da', 'DANISH'), ('de', 'GERMAN'), ('el', 'GREEK'), ('en-GB', 'BRITISH_ENGLISH'), ('en-IN', 'INDIAN_ENGLISH'), ('es', 'SPANISH'), ('es-419', 'LATIN_AMERICAN_SPANISH'), ('es-US', 'US_ENGLISH'), ('et', 'ESTONIAN'), ('eu', 'BASQUE'), ('fa', 'PERSIAN'), ('fi', 'FINNISH'), ('fil', 'FILIPINO'), ('fr-CA', 'CANADIAN_FRENCH'), ('fr', 'FRENCH'), ('gl', 'GALICIAN'), ('gu', 'GUJARATI'), ('hi', 'HINDI'), ('hr', 'CROATIAN'), ('hu', 'HUNGARIAN'), ('hy', 'ARMENIAN'), ('is', 'ICELANDIC'), ('it', 'ITALIAN'), ('iw', 'HEBREW'), ('jv', 'JAVANESE'), ('ka', 'GEORGIAN'), ('kk', 'KAZAKH'), ('km', 'KHMER'), ('kn', 'KANNADA'), ('ky', 'KYRGYZ'), ('lo', 'LAO'), ('lt', 'LITHUANIAN'), ('lv', 'LATVIAN'), ('mk', 'MACEDONIAN'), ('ml', 'MALAYALAM'), ('mn', 'MONGOLIAN'), ('mr', 'MARATHI'), ('ms', 'MALAY'), ('my', 'BURMESE'), ('no', 'NORWEGIAN'), ('ne', 'NEPALI'), ('nl', 'DUTCH'), ('or', 'ORIYA'), ('pa', 'PUNJABI'), ('pl', 'POLISH'), ('pt', 'PORTUGUESE'), ('pt-PT', 'PORTUGUESE_PORTUGAL'), ('ro', 'ROMANIAN'), ('ru', 'RUSSIAN'), ('si', 'SINHALESE'), ('sk', 'SLOVAK'), ('sl', 'SLOVENIAN'), ('sq', 'ALBANIAN'), ('sr-Latn', 'SERBIAN_LATIN'), ('sr', 'SERBIAN'), ('sv', 'SWEDISH'), ('sw', 'SWAHILI'), ('ta', 'TAMIL'), ('te', 'TELUGU'), ('th', 'THAI'), ('tr', 'TURKISH'), ('uk', 'UKRAINIAN'), ('ur', 'URDU'), ('uz', 'UZBEK'), ('vi', 'VIETNAMESE'), ('zh-Hans', 'CHINESE_SIMPLIFIED'), ('zh-HK', 'CHINESE_HONGKONG'), ('zh-TW', 'CHINESE_TRADITIONAL'), ('zu', 'ZULU')], max_length=20, verbose_name='言語コード')),
                ('documents', models.TextField(verbose_name='文書')),
                ('is_published', models.BooleanField(default=False, verbose_name='公開フラグ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.userdata', verbose_name='ユーザー')),
            ],
            options={
                'db_table': 'base_language',
            },
        ),
        migrations.CreateModel(
            name='LearningLanguage',
            fields=[
                ('learning_language_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='学習言語ID')),
                ('language_code', models.CharField(choices=[('ja', 'JAPANESE'), ('en', 'ENGLISH'), ('ko', 'KOREAN'), ('zh', 'CHINESE'), ('id', 'INDONESIAN'), ('af', 'AFRIKAANS'), ('am', 'AMHARIC'), ('ar', 'ARABIC'), ('as', 'ASSAMESE'), ('az', 'AZERBAIJANI'), ('be', 'BELARUSIAN'), ('bn', 'BENGALI'), ('bs', 'BOSNIAN'), ('ca', 'CATALAN'), ('cs', 'CZECH'), ('da', 'DANISH'), ('de', 'GERMAN'), ('el', 'GREEK'), ('en-GB', 'BRITISH_ENGLISH'), ('en-IN', 'INDIAN_ENGLISH'), ('es', 'SPANISH'), ('es-419', 'LATIN_AMERICAN_SPANISH'), ('es-US', 'US_ENGLISH'), ('et', 'ESTONIAN'), ('eu', 'BASQUE'), ('fa', 'PERSIAN'), ('fi', 'FINNISH'), ('fil', 'FILIPINO'), ('fr-CA', 'CANADIAN_FRENCH'), ('fr', 'FRENCH'), ('gl', 'GALICIAN'), ('gu', 'GUJARATI'), ('hi', 'HINDI'), ('hr', 'CROATIAN'), ('hu', 'HUNGARIAN'), ('hy', 'ARMENIAN'), ('is', 'ICELANDIC'), ('it', 'ITALIAN'), ('iw', 'HEBREW'), ('jv', 'JAVANESE'), ('ka', 'GEORGIAN'), ('kk', 'KAZAKH'), ('km', 'KHMER'), ('kn', 'KANNADA'), ('ky', 'KYRGYZ'), ('lo', 'LAO'), ('lt', 'LITHUANIAN'), ('lv', 'LATVIAN'), ('mk', 'MACEDONIAN'), ('ml', 'MALAYALAM'), ('mn', 'MONGOLIAN'), ('mr', 'MARATHI'), ('ms', 'MALAY'), ('my', 'BURMESE'), ('no', 'NORWEGIAN'), ('ne', 'NEPALI'), ('nl', 'DUTCH'), ('or', 'ORIYA'), ('pa', 'PUNJABI'), ('pl', 'POLISH'), ('pt', 'PORTUGUESE'), ('pt-PT', 'PORTUGUESE_PORTUGAL'), ('ro', 'ROMANIAN'), ('ru', 'RUSSIAN'), ('si', 'SINHALESE'), ('sk', 'SLOVAK'), ('sl', 'SLOVENIAN'), ('sq', 'ALBANIAN'), ('sr-Latn', 'SERBIAN_LATIN'), ('sr', 'SERBIAN'), ('sv', 'SWEDISH'), ('sw', 'SWAHILI'), ('ta', 'TAMIL'), ('te', 'TELUGU'), ('th', 'THAI'), ('tr', 'TURKISH'), ('uk', 'UKRAINIAN'), ('ur', 'URDU'), ('uz', 'UZBEK'), ('vi', 'VIETNAMESE'), ('zh-Hans', 'CHINESE_SIMPLIFIED'), ('zh-HK', 'CHINESE_HONGKONG'), ('zh-TW', 'CHINESE_TRADITIONAL'), ('zu', 'ZULU')], max_length=20, verbose_name='言語コード')),
                ('documents', models.TextField(verbose_name='文章')),
                ('explanation', models.TextField(verbose_name='文章の解説')),
                ('video_id', models.CharField(max_length=50, verbose_name='動画ID')),
                ('timestamp_ms', models.IntegerField(verbose_name='タイムスタンプ(ms)')),
                ('base_language_id', models.ForeignKey(db_column='base_language_id', on_delete=django.db.models.deletion.CASCADE, to='myapp.baselanguage', verbose_name='ベース言語ID')),
            ],
            options={
                'db_table': 'learning_language',
            },
        ),
    ]
