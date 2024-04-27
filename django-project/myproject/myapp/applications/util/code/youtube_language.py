import unittest
from enum import Enum


class YouTubeLanguage(Enum):
    JAPANESE = "ja"  # 日本語
    ENGLISH = "en"  # 英語
    KOREAN = "ko"  # 韓国語
    CHINESE = "zh"  # 中国語
    INDONESIAN = "id"  # インドネシア語


class TestYouTubeLanguage(unittest.TestCase):

    def test_japanese_code_value(self):
        self.assertEqual(YouTubeLanguage.JAPANESE.value, "ja")

    def test_english_code_value(self):
        self.assertEqual(YouTubeLanguage.ENGLISH.value, "en")

    def test_korean_code_value(self):
        self.assertEqual(YouTubeLanguage.KOREAN.value, "ko")

    def test_chinese_code_value(self):
        self.assertEqual(YouTubeLanguage.CHINESE.value, "zh")

    def test_indonesian_code_value(self):
        self.assertEqual(YouTubeLanguage.INDONESIAN.value, "id")

    def test_japanese_enum_value(self):
        self.assertEqual(YouTubeLanguage("ja"), YouTubeLanguage.JAPANESE)

    def test_english_enum_value(self):
        self.assertEqual(YouTubeLanguage("en"), YouTubeLanguage.ENGLISH)

    def test_korean_enum_value(self):
        self.assertEqual(YouTubeLanguage("ko"), YouTubeLanguage.KOREAN)

    def test_chinese_enum_value(self):
        self.assertEqual(YouTubeLanguage("zh"), YouTubeLanguage.CHINESE)

    def test_indonesian_enum_value(self):
        self.assertEqual(YouTubeLanguage("id"), YouTubeLanguage.INDONESIAN)


if __name__ == "__main__":
    unittest.main()
