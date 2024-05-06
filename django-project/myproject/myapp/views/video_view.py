from django.http import JsonResponse
from rest_framework.decorators import api_view

from myapp.applications.application.service.youtube_download_service import YoutubeDownloadService


@api_view(['GET'])
def get_video_data(request, video_id):
    youtube_download_service = YoutubeDownloadService()
    video_data = youtube_download_service.get_video_data(video_id)

    # TODO:一旦初期データ直接突っ込む（言語指定もできていない）
    youtube_download_service.insert_initial_subtitle_detail(video_id)

    response = youtube_download_service.get_video_subtitle_data(video_id)
    # JSONレスポンスを作成
    data = {
        "video_data": video_data,
        "response": response
    }

    return JsonResponse(data=data, status=200)
