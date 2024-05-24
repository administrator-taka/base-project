from django.http import JsonResponse
from rest_framework.decorators import api_view

from myapp.applications.application.service.youtube_download_service import YoutubeDownloadService


@api_view(['GET'])
def get_video_data(request, video_id):
    youtube_download_service = YoutubeDownloadService()
    video_data = youtube_download_service.get_video_data(video_id)

    youtube_download_service.insert_initial_subtitle_detail(video_id)

    subtitle_list = youtube_download_service.get_video_subtitle_data(video_id)
    # JSONレスポンスを作成
    data = {
        "video_data": video_data,
        "subtitle_list": subtitle_list
    }

    return JsonResponse(data=data, status=200)
