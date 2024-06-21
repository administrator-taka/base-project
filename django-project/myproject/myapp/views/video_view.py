from django.http import JsonResponse
from rest_framework.decorators import api_view

from myapp.applications.application.service.video_service import VideoService


@api_view(['GET'])
def get_video_data(request, video_id):
    youtube_download_service = VideoService()
    video_data = youtube_download_service.get_video_data(video_id)

    youtube_download_service.insert_initial_subtitle_detail(video_id)

    subtitle_list = youtube_download_service.get_video_subtitle_data(video_id)
    # JSONレスポンスを作成
    data = {
        "video_data": video_data,
        "subtitle_list": subtitle_list
    }

    return JsonResponse(data=data, status=200)


@api_view(['GET'])
def download_video_subtitle(request, video_id):
    youtube_download_service = VideoService()

    youtube_download_service.single_download_video_subtitle(video_id)
    # JSONレスポンスを作成
    data = {
        "status": 0,
    }

    return JsonResponse(data=data, status=200)
