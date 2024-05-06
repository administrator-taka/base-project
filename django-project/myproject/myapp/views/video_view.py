from django.http import JsonResponse
from rest_framework.decorators import api_view

from myapp.applications.application.service.youtube_download_service import YoutubeDownloadService
from myapp.applications.util.code.subtitle_type import SubtitleType


@api_view(['GET'])
def get_video_data(request, video_id):
    youtube_download_service = YoutubeDownloadService()
    video_data = youtube_download_service.get_video_data(video_id)
    # JSONレスポンスを作成
    data = {
        "video_data": video_data,
        "response": "response"
    }

    return JsonResponse(data=data, status=200)
