import unittest
from enum import Enum


class YouTubeLanguage(Enum):
    JAPANESE = "ja"  # 日本語
    ENGLISH = "en"  # 英語
    KOREAN = "ko"  # 韓国語
    INDONESIAN = "id"  # インドネシア語
    # 以下動作未確認
    AFRIKAANS = "af"
    AMHARIC = "am"
    ARABIC = "ar"
    ASSAMESE = "as"
    AZERBAIJANI = "az"
    BELARUSIAN = "be"
    BENGALI = "bn"
    BOSNIAN = "bs"
    CATALAN = "ca"
    CZECH = "cs"
    DANISH = "da"
    GERMAN = "de"
    GREEK = "el"
    BRITISH_ENGLISH = "en-GB"
    INDIAN_ENGLISH = "en-IN"
    ENGLISH = "en"
    SPANISH = "es"
    LATIN_AMERICAN_SPANISH = "es-419"
    US_ENGLISH = "es-US"
    ESTONIAN = "et"
    BASQUE = "eu"
    PERSIAN = "fa"
    FINNISH = "fi"
    FILIPINO = "fil"
    CANADIAN_FRENCH = "fr-CA"
    FRENCH = "fr"
    GALICIAN = "gl"
    GUJARATI = "gu"
    HINDI = "hi"
    CROATIAN = "hr"
    HUNGARIAN = "hu"
    ARMENIAN = "hy"
    ICELANDIC = "is"
    ITALIAN = "it"
    HEBREW = "iw"
    JAVANESE = "jv"
    GEORGIAN = "ka"
    KAZAKH = "kk"
    KHMER = "km"
    KANNADA = "kn"
    KYRGYZ = "ky"
    LAO = "lo"
    LITHUANIAN = "lt"
    LATVIAN = "lv"
    MACEDONIAN = "mk"
    MALAYALAM = "ml"
    MONGOLIAN = "mn"
    MARATHI = "mr"
    MALAY = "ms"
    BURMESE = "my"
    NORWEGIAN = "no"
    NEPALI = "ne"
    DUTCH = "nl"
    ORIYA = "or"
    PUNJABI = "pa"
    POLISH = "pl"
    PORTUGUESE = "pt"
    PORTUGUESE_PORTUGAL = "pt-PT"
    ROMANIAN = "ro"
    RUSSIAN = "ru"
    SINHALESE = "si"
    SLOVAK = "sk"
    SLOVENIAN = "sl"
    ALBANIAN = "sq"
    SERBIAN_LATIN = "sr-Latn"
    SERBIAN = "sr"
    SWEDISH = "sv"
    SWAHILI = "sw"
    TAMIL = "ta"
    TELUGU = "te"
    THAI = "th"
    TURKISH = "tr"
    UKRAINIAN = "uk"
    URDU = "ur"
    UZBEK = "uz"
    VIETNAMESE = "vi"
    CHINESE_SIMPLIFIED = "zh-CN"
    CHINESE_HONGKONG = "zh-HK"
    CHINESE_TRADITIONAL = "zh-TW"
    ZULU = "zu"


class TestYouTubeLanguage(unittest.TestCase):

    def test_japanese_code_value(self):
        self.assertEqual(YouTubeLanguage.JAPANESE.value, "ja")

    def test_english_code_value(self):
        self.assertEqual(YouTubeLanguage.ENGLISH.value, "en")

    def test_korean_code_value(self):
        self.assertEqual(YouTubeLanguage.KOREAN.value, "ko")

    def test_indonesian_code_value(self):
        self.assertEqual(YouTubeLanguage.INDONESIAN.value, "id")

    def test_japanese_enum_value(self):
        self.assertEqual(YouTubeLanguage("ja"), YouTubeLanguage.JAPANESE)

    def test_english_enum_value(self):
        self.assertEqual(YouTubeLanguage("en"), YouTubeLanguage.ENGLISH)

    def test_korean_enum_value(self):
        self.assertEqual(YouTubeLanguage("ko"), YouTubeLanguage.KOREAN)

    def test_indonesian_enum_value(self):
        self.assertEqual(YouTubeLanguage("id"), YouTubeLanguage.INDONESIAN)


if __name__ == "__main__":
    unittest.main()
