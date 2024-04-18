from enum import Enum
import unittest


class YouTubeLanguage(Enum):
    JAPANESE = "ja"  # 日本語
    ENGLISH = "en"  # 英語
    KOREAN = "ko"  # 韓国語
    CHINESE = "zh"  # 中国語
    INDONESIAN = "id"  # インドネシア語


# Enumの値を入れる処理
def set_language(language_code):
    for lang in YouTubeLanguage:
        if lang.value == language_code:
            return lang
    raise ValueError("Invalid language code")


class TestYouTubeLanguage(unittest.TestCase):
    def test_set_language_valid(self):
        code = "ja"
        enum_obj = set_language(code)
        self.assertEqual(enum_obj, YouTubeLanguage.JAPANESE)

    def test_set_language_invalid(self):
        with self.assertRaises(ValueError):
            set_language("fr")

    def test_enum_direct_assignment(self):
        korean_enum = YouTubeLanguage.KOREAN
        self.assertEqual(korean_enum, YouTubeLanguage.KOREAN)


if __name__ == "__main__":
    unittest.main()
