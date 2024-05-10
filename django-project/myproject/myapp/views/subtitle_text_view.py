from django.http import JsonResponse
from rest_framework.decorators import api_view

from myapp.applications.application.service.youtube_download_service import YoutubeDownloadService
from myapp.applications.util.code.youtube_language import YouTubeLanguage


@api_view(['POST'])
def get_subtitle_text_data(request, subtitle_text_id):
    # リクエストのJSONの中身を取得
    request_data = request.data

    language_code = request_data.get('language_code', None)

    youtube_download_service = YoutubeDownloadService()
    subtitle_text_data = youtube_download_service.get_subtitle_text_data(subtitle_text_id,
                                                                         YouTubeLanguage(language_code))

    # JSONレスポンスを作成
    data = {
        "subtitle_text_data": subtitle_text_data,
    }

    return JsonResponse(data=data, status=200)


@api_view(['POST'])
def update_subtitle_translation(request, subtitle_text_id):
    # リクエストのJSONの中身を取得
    request_data = request.data

    language_code = request_data.get('language_code', None)
    subtitle_transration_text = request_data.get('subtitle_transration_text', None)
    subtitle_transration_text_detail = request_data.get('subtitle_transration_text_detail', None)

    youtube_download_service = YoutubeDownloadService()
    youtube_download_service.update_subtitle_translation(subtitle_text_id,
                                                         YouTubeLanguage(language_code),
                                                         subtitle_transration_text,
                                                         subtitle_transration_text_detail)

    # JSONレスポンスを作成
    data = {
        "response": "response"
    }

    return JsonResponse(data=data, status=200)
