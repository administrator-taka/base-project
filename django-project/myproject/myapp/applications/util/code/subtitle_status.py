from enum import Enum


class SubtitleStatus(Enum):
    NO_SUBTITLE = 0  # 字幕なし
    REGISTERED = 1  # 字幕あり、登録済み
    UNREGISTERED = 2  # 字幕あり、未登録
    REGISTRATION_FAILED = 3  # 字幕あり、登録失敗
