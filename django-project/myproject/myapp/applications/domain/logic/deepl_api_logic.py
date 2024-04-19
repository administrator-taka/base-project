import unittest

import deepl

from myapp.applications.util.code.deepl_language import DeepLLanguage
from myproject.settings.base import DEEPL_API_KEY


class DeepLApiLogic:
    def __init__(self):
        # DeepLのAPIキーを読み込む
        self.api_key = DEEPL_API_KEY

    def translation(self, word, lang):
        translator = deepl.Translator(self.api_key)
        result = translator.translate_text(word, target_lang=lang)
        return result


class TestDeepLApiLogic(unittest.TestCase):
    def setUp(self):
        # 翻訳する単語をセットアップ
        self.word = "こんにちは。私は英語の勉強がしたいです。"

    def test_translation_japanese(self):
        # 日本語への翻訳をテスト
        lang = DeepLLanguage.JAPANESE
        deepl_logic = DeepLApiLogic()
        translated_word = deepl_logic.translation(self.word, lang.value)
        print(f"{lang.name}への翻訳: {translated_word}")

    def test_translation_english_gb(self):
        # 英語 (イギリス) への翻訳をテスト
        lang = DeepLLanguage.ENGLISH_GB
        deepl_logic = DeepLApiLogic()
        translated_word = deepl_logic.translation(self.word, lang.value)
        print(f"{lang.name}への翻訳: {translated_word}")

    def test_translation_english_us(self):
        # 英語 (アメリカ) への翻訳をテスト
        lang = DeepLLanguage.ENGLISH_US
        deepl_logic = DeepLApiLogic()
        translated_word = deepl_logic.translation(self.word, lang.value)
        print(f"{lang.name}への翻訳: {translated_word}")

    def test_translation_korean(self):
        # 韓国語への翻訳をテスト
        lang = DeepLLanguage.KOREAN
        deepl_logic = DeepLApiLogic()
        translated_word = deepl_logic.translation(self.word, lang.value)
        print(f"{lang.name}への翻訳: {translated_word}")

    def test_translation_chinese(self):
        # 中国語への翻訳をテスト
        lang = DeepLLanguage.CHINESE
        deepl_logic = DeepLApiLogic()
        translated_word = deepl_logic.translation(self.word, lang.value)
        print(f"{lang.name}への翻訳: {translated_word}")

    def test_translation_indonesian(self):
        # インドネシア語への翻訳をテスト
        lang = DeepLLanguage.INDONESIAN
        deepl_logic = DeepLApiLogic()
        translated_word = deepl_logic.translation(self.word, lang.value)
        print(f"{lang.name}への翻訳: {translated_word}")

# if __name__ == '__main__':
#     unittest.main()
