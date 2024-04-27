from enum import Enum


class SubtitleType(Enum):
    AUTOMATIC = 0
    MANUAL = 1

    def to_string(self):
        if self == SubtitleType.AUTOMATIC:
            return "automatic_captions"
        elif self == SubtitleType.MANUAL:
            return "subtitles"


# Enum要素から文字列への変換
auto_string = SubtitleType.AUTOMATIC.to_string()
print(auto_string)  # "automatic_captions"

manual_string = SubtitleType.MANUAL.to_string()
print(manual_string)  # "subtitles"
