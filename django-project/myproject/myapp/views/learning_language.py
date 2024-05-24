from django.http import JsonResponse
from rest_framework.decorators import api_view

from myapp.applications.application.service.learning_language_service import LearningLanguageService
from myapp.applications.util.code.learning_status import LearningStatus
from myapp.applications.util.code.youtube_language import YouTubeLanguage


@api_view(['POST'])
def get_learning_subtitle_text_list(request):
    # リクエストのJSONの中身を取得
    request_data = request.data

    language_code = request_data.get('language_code', None)
    learning_status = request_data.get('learning_status', None)

    learning_language_service = LearningLanguageService()
    learning_subtitle_list=learning_language_service.get_learning_subtitle_text_list(
        YouTubeLanguage(language_code),
        LearningStatus(learning_status))

    # JSONレスポンスを作成
    data = {
        "learning_subtitle_list": learning_subtitle_list
    }

    return JsonResponse(data=data, status=200)
