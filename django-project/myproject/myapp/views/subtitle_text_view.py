from django.http import JsonResponse
from rest_framework.decorators import api_view

from myapp.applications.application.service.subtitle_text_service import SubtitleTextService
from myapp.applications.util.code.learning_status import LearningStatus
from myapp.applications.util.code.youtube_language import YouTubeLanguage


@api_view(['POST'])
def get_subtitle_text_data(request, subtitle_text_id):
    # リクエストのJSONの中身を取得
    request_data = request.data

    language_code = request_data.get('language_code', None)

    user_id = request.user_id

    youtube_download_service = SubtitleTextService()
    subtitle_text_data = youtube_download_service.get_subtitle_text_data(subtitle_text_id,
                                                                         YouTubeLanguage(language_code), user_id)

    # JSONレスポンスを作成
    data = {
        "subtitle_text_data": subtitle_text_data,
    }

    return JsonResponse(data=data, status=200)


@api_view(['POST'])
def execute_chatgpt_translation(request, subtitle_text_id):
    # リクエストのJSONの中身を取得
    request_data = request.data

    language_code = request_data.get('language_code', None)

    call_api = request_data.get('call_api', False)

    youtube_download_service = SubtitleTextService()

    chatgpt_data = youtube_download_service.execute_chatgpt_translation(subtitle_text_id,
                                                                        YouTubeLanguage(language_code),
                                                                        call_api)

    # JSONレスポンスを作成
    data = {
        "chatgpt_data": chatgpt_data,
    }

    return JsonResponse(data=data, status=200)


@api_view(['POST'])
def update_subtitle_translation(request, subtitle_text_id):
    # リクエストのJSONの中身を取得
    request_data = request.data

    language_code = request_data.get('language_code', None)
    subtitle_literal_translation_text = request_data.get('subtitle_literal_translation_text', None)
    subtitle_translation_text_detail = request_data.get('subtitle_translation_text_detail', None)

    youtube_download_service = SubtitleTextService()
    youtube_download_service.update_subtitle_translation(subtitle_text_id,
                                                         YouTubeLanguage(language_code),
                                                         subtitle_literal_translation_text,
                                                         subtitle_translation_text_detail)

    # JSONレスポンスを作成
    data = {
        "status": 0
    }

    return JsonResponse(data=data, status=200)


@api_view(['POST'])
def insert_or_update_subtitle_learning_memory(request, subtitle_text_id):
    # リクエストのJSONの中身を取得
    request_data = request.data

    language_code = request_data.get('language_code', None)
    learning_status = request_data.get('learning_status', None)
    favorite = request_data.get('favorite', False)
    user_id = request.user_id

    youtube_download_service = SubtitleTextService()
    youtube_download_service.insert_or_update_subtitle_learning_memory(subtitle_text_id,
                                                                       YouTubeLanguage(language_code),
                                                                       LearningStatus(learning_status), user_id,
                                                                       favorite)

    # JSONレスポンスを作成
    data = {
        "status": 0
    }

    return JsonResponse(data=data, status=200)
