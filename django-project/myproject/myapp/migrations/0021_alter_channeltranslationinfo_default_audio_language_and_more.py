# Generated by Django 5.0.4 on 2024-05-05 10:24

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0020_remove_videosubtitleinfo_has_subtitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channeltranslationinfo',
            name='default_audio_language',
            field=models.CharField(choices=[('ja', 'JAPANESE'), ('en', 'ENGLISH'), ('ko', 'KOREAN'), ('zh', 'CHINESE'),
                                            ('id', 'INDONESIAN'), ('af', 'AFRIKAANS'), ('am', 'AMHARIC'),
                                            ('ar', 'ARABIC'), ('as', 'ASSAMESE'), ('az', 'AZERBAIJANI'),
                                            ('be', 'BELARUSIAN'), ('bn', 'BENGALI'), ('bs', 'BOSNIAN'),
                                            ('ca', 'CATALAN'), ('cs', 'CZECH'), ('da', 'DANISH'), ('de', 'GERMAN'),
                                            ('el', 'GREEK'), ('en-GB', 'BRITISH_ENGLISH'), ('en-IN', 'INDIAN_ENGLISH'),
                                            ('es', 'SPANISH'), ('es-419', 'LATIN_AMERICAN_SPANISH'),
                                            ('es-US', 'US_ENGLISH'), ('et', 'ESTONIAN'), ('eu', 'BASQUE'),
                                            ('fa', 'PERSIAN'), ('fi', 'FINNISH'), ('fil', 'FILIPINO'),
                                            ('fr-CA', 'CANADIAN_FRENCH'), ('fr', 'FRENCH'), ('gl', 'GALICIAN'),
                                            ('gu', 'GUJARATI'), ('hi', 'HINDI'), ('hr', 'CROATIAN'),
                                            ('hu', 'HUNGARIAN'), ('hy', 'ARMENIAN'), ('is', 'ICELANDIC'),
                                            ('it', 'ITALIAN'), ('iw', 'HEBREW'), ('jv', 'JAVANESE'), ('ka', 'GEORGIAN'),
                                            ('kk', 'KAZAKH'), ('km', 'KHMER'), ('kn', 'KANNADA'), ('ky', 'KYRGYZ'),
                                            ('lo', 'LAO'), ('lt', 'LITHUANIAN'), ('lv', 'LATVIAN'),
                                            ('mk', 'MACEDONIAN'), ('ml', 'MALAYALAM'), ('mn', 'MONGOLIAN'),
                                            ('mr', 'MARATHI'), ('ms', 'MALAY'), ('my', 'BURMESE'), ('no', 'NORWEGIAN'),
                                            ('ne', 'NEPALI'), ('nl', 'DUTCH'), ('or', 'ORIYA'), ('pa', 'PUNJABI'),
                                            ('pl', 'POLISH'), ('pt', 'PORTUGUESE'), ('pt-PT', 'PORTUGUESE_PORTUGAL'),
                                            ('ro', 'ROMANIAN'), ('ru', 'RUSSIAN'), ('si', 'SINHALESE'),
                                            ('sk', 'SLOVAK'), ('sl', 'SLOVENIAN'), ('sq', 'ALBANIAN'),
                                            ('sr-Latn', 'SERBIAN_LATIN'), ('sr', 'SERBIAN'), ('sv', 'SWEDISH'),
                                            ('sw', 'SWAHILI'), ('ta', 'TAMIL'), ('te', 'TELUGU'), ('th', 'THAI'),
                                            ('tr', 'TURKISH'), ('uk', 'UKRAINIAN'), ('ur', 'URDU'), ('uz', 'UZBEK'),
                                            ('vi', 'VIETNAMESE'), ('zh-CN', 'CHINESE_SIMPLIFIED'),
                                            ('zh-HK', 'CHINESE_HONGKONG'), ('zh-TW', 'CHINESE_TRADITIONAL'),
                                            ('zu', 'ZULU')], null=True, verbose_name='デフォルトの言語コード'),
        ),
        migrations.AlterField(
            model_name='channeltranslationinfo',
            name='translation_languages',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(
                choices=[('ja', 'JAPANESE'), ('en', 'ENGLISH'), ('ko', 'KOREAN'), ('zh', 'CHINESE'),
                         ('id', 'INDONESIAN'), ('af', 'AFRIKAANS'), ('am', 'AMHARIC'), ('ar', 'ARABIC'),
                         ('as', 'ASSAMESE'), ('az', 'AZERBAIJANI'), ('be', 'BELARUSIAN'), ('bn', 'BENGALI'),
                         ('bs', 'BOSNIAN'), ('ca', 'CATALAN'), ('cs', 'CZECH'), ('da', 'DANISH'), ('de', 'GERMAN'),
                         ('el', 'GREEK'), ('en-GB', 'BRITISH_ENGLISH'), ('en-IN', 'INDIAN_ENGLISH'), ('es', 'SPANISH'),
                         ('es-419', 'LATIN_AMERICAN_SPANISH'), ('es-US', 'US_ENGLISH'), ('et', 'ESTONIAN'),
                         ('eu', 'BASQUE'), ('fa', 'PERSIAN'), ('fi', 'FINNISH'), ('fil', 'FILIPINO'),
                         ('fr-CA', 'CANADIAN_FRENCH'), ('fr', 'FRENCH'), ('gl', 'GALICIAN'), ('gu', 'GUJARATI'),
                         ('hi', 'HINDI'), ('hr', 'CROATIAN'), ('hu', 'HUNGARIAN'), ('hy', 'ARMENIAN'),
                         ('is', 'ICELANDIC'), ('it', 'ITALIAN'), ('iw', 'HEBREW'), ('jv', 'JAVANESE'),
                         ('ka', 'GEORGIAN'), ('kk', 'KAZAKH'), ('km', 'KHMER'), ('kn', 'KANNADA'), ('ky', 'KYRGYZ'),
                         ('lo', 'LAO'), ('lt', 'LITHUANIAN'), ('lv', 'LATVIAN'), ('mk', 'MACEDONIAN'),
                         ('ml', 'MALAYALAM'), ('mn', 'MONGOLIAN'), ('mr', 'MARATHI'), ('ms', 'MALAY'),
                         ('my', 'BURMESE'), ('no', 'NORWEGIAN'), ('ne', 'NEPALI'), ('nl', 'DUTCH'), ('or', 'ORIYA'),
                         ('pa', 'PUNJABI'), ('pl', 'POLISH'), ('pt', 'PORTUGUESE'), ('pt-PT', 'PORTUGUESE_PORTUGAL'),
                         ('ro', 'ROMANIAN'), ('ru', 'RUSSIAN'), ('si', 'SINHALESE'), ('sk', 'SLOVAK'),
                         ('sl', 'SLOVENIAN'), ('sq', 'ALBANIAN'), ('sr-Latn', 'SERBIAN_LATIN'), ('sr', 'SERBIAN'),
                         ('sv', 'SWEDISH'), ('sw', 'SWAHILI'), ('ta', 'TAMIL'), ('te', 'TELUGU'), ('th', 'THAI'),
                         ('tr', 'TURKISH'), ('uk', 'UKRAINIAN'), ('ur', 'URDU'), ('uz', 'UZBEK'), ('vi', 'VIETNAMESE'),
                         ('zh-CN', 'CHINESE_SIMPLIFIED'), ('zh-HK', 'CHINESE_HONGKONG'),
                         ('zh-TW', 'CHINESE_TRADITIONAL'), ('zu', 'ZULU')], max_length=10), null=True, size=None,
                                                            verbose_name='翻訳の言語コードリスト'),
        ),
        migrations.AlterField(
            model_name='subtitletranslation',
            name='language_code',
            field=models.CharField(choices=[('ja', 'JAPANESE'), ('en', 'ENGLISH'), ('ko', 'KOREAN'), ('zh', 'CHINESE'),
                                            ('id', 'INDONESIAN'), ('af', 'AFRIKAANS'), ('am', 'AMHARIC'),
                                            ('ar', 'ARABIC'), ('as', 'ASSAMESE'), ('az', 'AZERBAIJANI'),
                                            ('be', 'BELARUSIAN'), ('bn', 'BENGALI'), ('bs', 'BOSNIAN'),
                                            ('ca', 'CATALAN'), ('cs', 'CZECH'), ('da', 'DANISH'), ('de', 'GERMAN'),
                                            ('el', 'GREEK'), ('en-GB', 'BRITISH_ENGLISH'), ('en-IN', 'INDIAN_ENGLISH'),
                                            ('es', 'SPANISH'), ('es-419', 'LATIN_AMERICAN_SPANISH'),
                                            ('es-US', 'US_ENGLISH'), ('et', 'ESTONIAN'), ('eu', 'BASQUE'),
                                            ('fa', 'PERSIAN'), ('fi', 'FINNISH'), ('fil', 'FILIPINO'),
                                            ('fr-CA', 'CANADIAN_FRENCH'), ('fr', 'FRENCH'), ('gl', 'GALICIAN'),
                                            ('gu', 'GUJARATI'), ('hi', 'HINDI'), ('hr', 'CROATIAN'),
                                            ('hu', 'HUNGARIAN'), ('hy', 'ARMENIAN'), ('is', 'ICELANDIC'),
                                            ('it', 'ITALIAN'), ('iw', 'HEBREW'), ('jv', 'JAVANESE'), ('ka', 'GEORGIAN'),
                                            ('kk', 'KAZAKH'), ('km', 'KHMER'), ('kn', 'KANNADA'), ('ky', 'KYRGYZ'),
                                            ('lo', 'LAO'), ('lt', 'LITHUANIAN'), ('lv', 'LATVIAN'),
                                            ('mk', 'MACEDONIAN'), ('ml', 'MALAYALAM'), ('mn', 'MONGOLIAN'),
                                            ('mr', 'MARATHI'), ('ms', 'MALAY'), ('my', 'BURMESE'), ('no', 'NORWEGIAN'),
                                            ('ne', 'NEPALI'), ('nl', 'DUTCH'), ('or', 'ORIYA'), ('pa', 'PUNJABI'),
                                            ('pl', 'POLISH'), ('pt', 'PORTUGUESE'), ('pt-PT', 'PORTUGUESE_PORTUGAL'),
                                            ('ro', 'ROMANIAN'), ('ru', 'RUSSIAN'), ('si', 'SINHALESE'),
                                            ('sk', 'SLOVAK'), ('sl', 'SLOVENIAN'), ('sq', 'ALBANIAN'),
                                            ('sr-Latn', 'SERBIAN_LATIN'), ('sr', 'SERBIAN'), ('sv', 'SWEDISH'),
                                            ('sw', 'SWAHILI'), ('ta', 'TAMIL'), ('te', 'TELUGU'), ('th', 'THAI'),
                                            ('tr', 'TURKISH'), ('uk', 'UKRAINIAN'), ('ur', 'URDU'), ('uz', 'UZBEK'),
                                            ('vi', 'VIETNAMESE'), ('zh-CN', 'CHINESE_SIMPLIFIED'),
                                            ('zh-HK', 'CHINESE_HONGKONG'), ('zh-TW', 'CHINESE_TRADITIONAL'),
                                            ('zu', 'ZULU')], verbose_name='言語コード'),
        ),
        migrations.AlterField(
            model_name='videodetail',
            name='default_audio_language',
            field=models.CharField(choices=[('ja', 'JAPANESE'), ('en', 'ENGLISH'), ('ko', 'KOREAN'), ('zh', 'CHINESE'),
                                            ('id', 'INDONESIAN'), ('af', 'AFRIKAANS'), ('am', 'AMHARIC'),
                                            ('ar', 'ARABIC'), ('as', 'ASSAMESE'), ('az', 'AZERBAIJANI'),
                                            ('be', 'BELARUSIAN'), ('bn', 'BENGALI'), ('bs', 'BOSNIAN'),
                                            ('ca', 'CATALAN'), ('cs', 'CZECH'), ('da', 'DANISH'), ('de', 'GERMAN'),
                                            ('el', 'GREEK'), ('en-GB', 'BRITISH_ENGLISH'), ('en-IN', 'INDIAN_ENGLISH'),
                                            ('es', 'SPANISH'), ('es-419', 'LATIN_AMERICAN_SPANISH'),
                                            ('es-US', 'US_ENGLISH'), ('et', 'ESTONIAN'), ('eu', 'BASQUE'),
                                            ('fa', 'PERSIAN'), ('fi', 'FINNISH'), ('fil', 'FILIPINO'),
                                            ('fr-CA', 'CANADIAN_FRENCH'), ('fr', 'FRENCH'), ('gl', 'GALICIAN'),
                                            ('gu', 'GUJARATI'), ('hi', 'HINDI'), ('hr', 'CROATIAN'),
                                            ('hu', 'HUNGARIAN'), ('hy', 'ARMENIAN'), ('is', 'ICELANDIC'),
                                            ('it', 'ITALIAN'), ('iw', 'HEBREW'), ('jv', 'JAVANESE'), ('ka', 'GEORGIAN'),
                                            ('kk', 'KAZAKH'), ('km', 'KHMER'), ('kn', 'KANNADA'), ('ky', 'KYRGYZ'),
                                            ('lo', 'LAO'), ('lt', 'LITHUANIAN'), ('lv', 'LATVIAN'),
                                            ('mk', 'MACEDONIAN'), ('ml', 'MALAYALAM'), ('mn', 'MONGOLIAN'),
                                            ('mr', 'MARATHI'), ('ms', 'MALAY'), ('my', 'BURMESE'), ('no', 'NORWEGIAN'),
                                            ('ne', 'NEPALI'), ('nl', 'DUTCH'), ('or', 'ORIYA'), ('pa', 'PUNJABI'),
                                            ('pl', 'POLISH'), ('pt', 'PORTUGUESE'), ('pt-PT', 'PORTUGUESE_PORTUGAL'),
                                            ('ro', 'ROMANIAN'), ('ru', 'RUSSIAN'), ('si', 'SINHALESE'),
                                            ('sk', 'SLOVAK'), ('sl', 'SLOVENIAN'), ('sq', 'ALBANIAN'),
                                            ('sr-Latn', 'SERBIAN_LATIN'), ('sr', 'SERBIAN'), ('sv', 'SWEDISH'),
                                            ('sw', 'SWAHILI'), ('ta', 'TAMIL'), ('te', 'TELUGU'), ('th', 'THAI'),
                                            ('tr', 'TURKISH'), ('uk', 'UKRAINIAN'), ('ur', 'URDU'), ('uz', 'UZBEK'),
                                            ('vi', 'VIETNAMESE'), ('zh-CN', 'CHINESE_SIMPLIFIED'),
                                            ('zh-HK', 'CHINESE_HONGKONG'), ('zh-TW', 'CHINESE_TRADITIONAL'),
                                            ('zu', 'ZULU')], null=True, verbose_name='デフォルトの言語コード'),
        ),
        migrations.AlterField(
            model_name='videodetail',
            name='default_language',
            field=models.CharField(choices=[('ja', 'JAPANESE'), ('en', 'ENGLISH'), ('ko', 'KOREAN'), ('zh', 'CHINESE'),
                                            ('id', 'INDONESIAN'), ('af', 'AFRIKAANS'), ('am', 'AMHARIC'),
                                            ('ar', 'ARABIC'), ('as', 'ASSAMESE'), ('az', 'AZERBAIJANI'),
                                            ('be', 'BELARUSIAN'), ('bn', 'BENGALI'), ('bs', 'BOSNIAN'),
                                            ('ca', 'CATALAN'), ('cs', 'CZECH'), ('da', 'DANISH'), ('de', 'GERMAN'),
                                            ('el', 'GREEK'), ('en-GB', 'BRITISH_ENGLISH'), ('en-IN', 'INDIAN_ENGLISH'),
                                            ('es', 'SPANISH'), ('es-419', 'LATIN_AMERICAN_SPANISH'),
                                            ('es-US', 'US_ENGLISH'), ('et', 'ESTONIAN'), ('eu', 'BASQUE'),
                                            ('fa', 'PERSIAN'), ('fi', 'FINNISH'), ('fil', 'FILIPINO'),
                                            ('fr-CA', 'CANADIAN_FRENCH'), ('fr', 'FRENCH'), ('gl', 'GALICIAN'),
                                            ('gu', 'GUJARATI'), ('hi', 'HINDI'), ('hr', 'CROATIAN'),
                                            ('hu', 'HUNGARIAN'), ('hy', 'ARMENIAN'), ('is', 'ICELANDIC'),
                                            ('it', 'ITALIAN'), ('iw', 'HEBREW'), ('jv', 'JAVANESE'), ('ka', 'GEORGIAN'),
                                            ('kk', 'KAZAKH'), ('km', 'KHMER'), ('kn', 'KANNADA'), ('ky', 'KYRGYZ'),
                                            ('lo', 'LAO'), ('lt', 'LITHUANIAN'), ('lv', 'LATVIAN'),
                                            ('mk', 'MACEDONIAN'), ('ml', 'MALAYALAM'), ('mn', 'MONGOLIAN'),
                                            ('mr', 'MARATHI'), ('ms', 'MALAY'), ('my', 'BURMESE'), ('no', 'NORWEGIAN'),
                                            ('ne', 'NEPALI'), ('nl', 'DUTCH'), ('or', 'ORIYA'), ('pa', 'PUNJABI'),
                                            ('pl', 'POLISH'), ('pt', 'PORTUGUESE'), ('pt-PT', 'PORTUGUESE_PORTUGAL'),
                                            ('ro', 'ROMANIAN'), ('ru', 'RUSSIAN'), ('si', 'SINHALESE'),
                                            ('sk', 'SLOVAK'), ('sl', 'SLOVENIAN'), ('sq', 'ALBANIAN'),
                                            ('sr-Latn', 'SERBIAN_LATIN'), ('sr', 'SERBIAN'), ('sv', 'SWEDISH'),
                                            ('sw', 'SWAHILI'), ('ta', 'TAMIL'), ('te', 'TELUGU'), ('th', 'THAI'),
                                            ('tr', 'TURKISH'), ('uk', 'UKRAINIAN'), ('ur', 'URDU'), ('uz', 'UZBEK'),
                                            ('vi', 'VIETNAMESE'), ('zh-CN', 'CHINESE_SIMPLIFIED'),
                                            ('zh-HK', 'CHINESE_HONGKONG'), ('zh-TW', 'CHINESE_TRADITIONAL'),
                                            ('zu', 'ZULU')], null=True, verbose_name='デフォルトのテキスト言語コード'),
        ),
        migrations.AlterField(
            model_name='videolocalized',
            name='language_code',
            field=models.CharField(choices=[('ja', 'JAPANESE'), ('en', 'ENGLISH'), ('ko', 'KOREAN'), ('zh', 'CHINESE'),
                                            ('id', 'INDONESIAN'), ('af', 'AFRIKAANS'), ('am', 'AMHARIC'),
                                            ('ar', 'ARABIC'), ('as', 'ASSAMESE'), ('az', 'AZERBAIJANI'),
                                            ('be', 'BELARUSIAN'), ('bn', 'BENGALI'), ('bs', 'BOSNIAN'),
                                            ('ca', 'CATALAN'), ('cs', 'CZECH'), ('da', 'DANISH'), ('de', 'GERMAN'),
                                            ('el', 'GREEK'), ('en-GB', 'BRITISH_ENGLISH'), ('en-IN', 'INDIAN_ENGLISH'),
                                            ('es', 'SPANISH'), ('es-419', 'LATIN_AMERICAN_SPANISH'),
                                            ('es-US', 'US_ENGLISH'), ('et', 'ESTONIAN'), ('eu', 'BASQUE'),
                                            ('fa', 'PERSIAN'), ('fi', 'FINNISH'), ('fil', 'FILIPINO'),
                                            ('fr-CA', 'CANADIAN_FRENCH'), ('fr', 'FRENCH'), ('gl', 'GALICIAN'),
                                            ('gu', 'GUJARATI'), ('hi', 'HINDI'), ('hr', 'CROATIAN'),
                                            ('hu', 'HUNGARIAN'), ('hy', 'ARMENIAN'), ('is', 'ICELANDIC'),
                                            ('it', 'ITALIAN'), ('iw', 'HEBREW'), ('jv', 'JAVANESE'), ('ka', 'GEORGIAN'),
                                            ('kk', 'KAZAKH'), ('km', 'KHMER'), ('kn', 'KANNADA'), ('ky', 'KYRGYZ'),
                                            ('lo', 'LAO'), ('lt', 'LITHUANIAN'), ('lv', 'LATVIAN'),
                                            ('mk', 'MACEDONIAN'), ('ml', 'MALAYALAM'), ('mn', 'MONGOLIAN'),
                                            ('mr', 'MARATHI'), ('ms', 'MALAY'), ('my', 'BURMESE'), ('no', 'NORWEGIAN'),
                                            ('ne', 'NEPALI'), ('nl', 'DUTCH'), ('or', 'ORIYA'), ('pa', 'PUNJABI'),
                                            ('pl', 'POLISH'), ('pt', 'PORTUGUESE'), ('pt-PT', 'PORTUGUESE_PORTUGAL'),
                                            ('ro', 'ROMANIAN'), ('ru', 'RUSSIAN'), ('si', 'SINHALESE'),
                                            ('sk', 'SLOVAK'), ('sl', 'SLOVENIAN'), ('sq', 'ALBANIAN'),
                                            ('sr-Latn', 'SERBIAN_LATIN'), ('sr', 'SERBIAN'), ('sv', 'SWEDISH'),
                                            ('sw', 'SWAHILI'), ('ta', 'TAMIL'), ('te', 'TELUGU'), ('th', 'THAI'),
                                            ('tr', 'TURKISH'), ('uk', 'UKRAINIAN'), ('ur', 'URDU'), ('uz', 'UZBEK'),
                                            ('vi', 'VIETNAMESE'), ('zh-CN', 'CHINESE_SIMPLIFIED'),
                                            ('zh-HK', 'CHINESE_HONGKONG'), ('zh-TW', 'CHINESE_TRADITIONAL'),
                                            ('zu', 'ZULU')], verbose_name='言語コード'),
        ),
        migrations.AlterField(
            model_name='videosubtitleinfo',
            name='language_code',
            field=models.CharField(choices=[('ja', 'JAPANESE'), ('en', 'ENGLISH'), ('ko', 'KOREAN'), ('zh', 'CHINESE'),
                                            ('id', 'INDONESIAN'), ('af', 'AFRIKAANS'), ('am', 'AMHARIC'),
                                            ('ar', 'ARABIC'), ('as', 'ASSAMESE'), ('az', 'AZERBAIJANI'),
                                            ('be', 'BELARUSIAN'), ('bn', 'BENGALI'), ('bs', 'BOSNIAN'),
                                            ('ca', 'CATALAN'), ('cs', 'CZECH'), ('da', 'DANISH'), ('de', 'GERMAN'),
                                            ('el', 'GREEK'), ('en-GB', 'BRITISH_ENGLISH'), ('en-IN', 'INDIAN_ENGLISH'),
                                            ('es', 'SPANISH'), ('es-419', 'LATIN_AMERICAN_SPANISH'),
                                            ('es-US', 'US_ENGLISH'), ('et', 'ESTONIAN'), ('eu', 'BASQUE'),
                                            ('fa', 'PERSIAN'), ('fi', 'FINNISH'), ('fil', 'FILIPINO'),
                                            ('fr-CA', 'CANADIAN_FRENCH'), ('fr', 'FRENCH'), ('gl', 'GALICIAN'),
                                            ('gu', 'GUJARATI'), ('hi', 'HINDI'), ('hr', 'CROATIAN'),
                                            ('hu', 'HUNGARIAN'), ('hy', 'ARMENIAN'), ('is', 'ICELANDIC'),
                                            ('it', 'ITALIAN'), ('iw', 'HEBREW'), ('jv', 'JAVANESE'), ('ka', 'GEORGIAN'),
                                            ('kk', 'KAZAKH'), ('km', 'KHMER'), ('kn', 'KANNADA'), ('ky', 'KYRGYZ'),
                                            ('lo', 'LAO'), ('lt', 'LITHUANIAN'), ('lv', 'LATVIAN'),
                                            ('mk', 'MACEDONIAN'), ('ml', 'MALAYALAM'), ('mn', 'MONGOLIAN'),
                                            ('mr', 'MARATHI'), ('ms', 'MALAY'), ('my', 'BURMESE'), ('no', 'NORWEGIAN'),
                                            ('ne', 'NEPALI'), ('nl', 'DUTCH'), ('or', 'ORIYA'), ('pa', 'PUNJABI'),
                                            ('pl', 'POLISH'), ('pt', 'PORTUGUESE'), ('pt-PT', 'PORTUGUESE_PORTUGAL'),
                                            ('ro', 'ROMANIAN'), ('ru', 'RUSSIAN'), ('si', 'SINHALESE'),
                                            ('sk', 'SLOVAK'), ('sl', 'SLOVENIAN'), ('sq', 'ALBANIAN'),
                                            ('sr-Latn', 'SERBIAN_LATIN'), ('sr', 'SERBIAN'), ('sv', 'SWEDISH'),
                                            ('sw', 'SWAHILI'), ('ta', 'TAMIL'), ('te', 'TELUGU'), ('th', 'THAI'),
                                            ('tr', 'TURKISH'), ('uk', 'UKRAINIAN'), ('ur', 'URDU'), ('uz', 'UZBEK'),
                                            ('vi', 'VIETNAMESE'), ('zh-CN', 'CHINESE_SIMPLIFIED'),
                                            ('zh-HK', 'CHINESE_HONGKONG'), ('zh-TW', 'CHINESE_TRADITIONAL'),
                                            ('zu', 'ZULU')], verbose_name='言語コード'),
        ),
        migrations.AlterField(
            model_name='videosubtitleinfo',
            name='subtitle_status',
            field=models.IntegerField(choices=[(0, 'NO_SUBTITLE'), (1, 'REGISTERED'), (2, 'UNREGISTERED')],
                                      verbose_name='字幕ステータス'),
        ),
    ]
