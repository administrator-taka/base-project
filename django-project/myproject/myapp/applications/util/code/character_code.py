import unittest
from enum import Enum


class CharacterCode(Enum):
    KS_X_1001 = "KS X 1001"  # 韓国語文字コード
    SHIFT_JIS = "Shift-JIS"  # 日本語文字コード
    GB2312 = "GB2312"  # 中国語文字コード
    UTF8 = "UTF-8"  # 英語文字コード (UTF-8は英語を含む多くの言語で使用される)
    ISO_8859_1 = "ISO-8859-1"  # インドネシア語文字コード (ISO-8859-1は西ヨーロッパ言語で広く使用されています)
    # 他の文字コードを追加する場合はここに追加する


# TODO:文字コードについて理解できていない
class TestStringEncoding(unittest.TestCase):
    def encode_as(self, string_to_encode, code):
        return string_to_encode.encode(code.value)

    def decode_as(self, encoded_string, code):
        return encoded_string.decode(code.value)

    def test_encode_decode_korean(self):
        string_to_encode = "안녕하세요, 세계!"  # 韓国語文字列
        encoded_string = self.encode_as(string_to_encode, CharacterCode.UTF8)
        decoded_string = self.decode_as(encoded_string, CharacterCode.UTF8)
        self.assertEqual(decoded_string, string_to_encode)

    def test_encode_decode_japanese(self):
        string_to_encode = "こんにちは、世界！"  # 日本語文字列
        encoded_string = self.encode_as(string_to_encode, CharacterCode.UTF8)
        decoded_string = self.decode_as(encoded_string, CharacterCode.UTF8)
        self.assertEqual(decoded_string, string_to_encode)

    def test_encode_decode_chinese(self):
        string_to_encode = "你好，世界！"  # 中国語文字列
        # 例えば你好，我想学习英语。我想学习英语。のフォントがおかしいのはどうしたらいい。
        encoded_string = self.encode_as(string_to_encode, CharacterCode.UTF8)
        decoded_string = self.decode_as(encoded_string, CharacterCode.UTF8)
        self.assertEqual(decoded_string, string_to_encode)

    def test_encode_decode_english(self):
        string_to_encode = "Hello, World!"  # 英語文字列
        encoded_string = self.encode_as(string_to_encode, CharacterCode.UTF8)
        decoded_string = self.decode_as(encoded_string, CharacterCode.UTF8)
        self.assertEqual(decoded_string, string_to_encode)

    def test_encode_decode_indonesian(self):
        string_to_encode = "Halo, Dunia!"  # インドネシア語文字列
        encoded_string = self.encode_as(string_to_encode, CharacterCode.UTF8)
        decoded_string = self.decode_as(encoded_string, CharacterCode.UTF8)
        self.assertEqual(decoded_string, string_to_encode)


if __name__ == '__main__':
    unittest.main()
