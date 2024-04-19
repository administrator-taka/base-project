import unittest
from enum import Enum


class DeepLLanguage(Enum):
    JAPANESE = "ja"  # 日本語
    ENGLISH_GB = "en-GB"  # 英語 (イギリス)
    ENGLISH_US = "en-US"  # 英語 (アメリカ)
    KOREAN = "ko"  # 韓国語
    CHINESE = "zh"  # 中国語
    INDONESIAN = "id"  # インドネシア語


# メモ
# 原文の言語は中国語（繁体字および簡体字）
# 訳文の言語は中国語（簡体字のみ）となります。

class TestDeepLLanguage(unittest.TestCase):
    def test_enum_values(self):
        self.assertEqual(DeepLLanguage.JAPANESE.value, "ja")
        self.assertEqual(DeepLLanguage.ENGLISH_GB.value, "en-GB")
        self.assertEqual(DeepLLanguage.ENGLISH_US.value, "en-US")
        self.assertEqual(DeepLLanguage.KOREAN.value, "ko")
        self.assertEqual(DeepLLanguage.CHINESE.value, "zh")
        self.assertEqual(DeepLLanguage.INDONESIAN.value, "id")


if __name__ == '__main__':
    unittest.main()
