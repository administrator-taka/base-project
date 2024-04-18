from enum import Enum


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


# 使用例
code = "ja"
enum_obj = set_language(code)
print(enum_obj.value)  # 出力: ja

# Enumを直接指定する
korean_enum = YouTubeLanguage.KOREAN

print(korean_enum.value)  # 出力: ko
