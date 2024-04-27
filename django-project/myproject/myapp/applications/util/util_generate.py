from myapp.applications.util.code.subtitle_type import SubtitleType
from myapp.applications.util.code.youtube_language import YouTubeLanguage
import uuid


def generate_subtitle_id(video_id: str, subtitle_type: SubtitleType, language: YouTubeLanguage):
    # 各値を文字列に変換して連結
    return f"{video_id}{subtitle_type.value}{language.value}"


def generate_uuid():
    """
    英大文字半角数字でUUIDを生成する。

    Returns:
        str: 英大文字半角数字で構成されたUUID。
    """
    return str(uuid.uuid4().hex.upper())
