from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from myapp.applications.application.service.youtube_download_service import YoutubeDownloadService
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myproject.settings.base import TEST_YOUTUBE_VIDEO_ID, TEST_YOUTUBE_CHANNEL_ID


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    test_2()
    return JsonResponse(data={"msg": "pass"}, status=200)


def test_1():
    youtube_download_service = YoutubeDownloadService()
    video_id = TEST_YOUTUBE_VIDEO_ID
    default_audio_language = YouTubeLanguage.KOREAN
    translation_language = YouTubeLanguage.JAPANESE

    youtube_download_service.download_video_subtitle(video_id, default_audio_language, translation_language)


def test_2():
    youtube_download_service = YoutubeDownloadService()

    channel_id = TEST_YOUTUBE_CHANNEL_ID

    youtube_download_service.download_channel_subtitles(channel_id)
