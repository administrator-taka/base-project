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

    user_id = request.user_id

    learning_language_service = LearningLanguageService()
    learning_subtitle_list = learning_language_service.get_learning_subtitle_text_list(
        YouTubeLanguage(language_code),
        LearningStatus(learning_status), user_id)

    # JSONレスポンスを作成
    data = {
        "learning_subtitle_list": learning_subtitle_list
    }

    return JsonResponse(data=data, status=200)


@api_view(['POST'])
def get_favorite_subtitle_text_list(request):
    # リクエストのJSONの中身を取得
    request_data = request.data

    language_code = request_data.get('language_code', None)

    user_id = request.user_id

    learning_language_service = LearningLanguageService()
    favorite_subtitle_list = learning_language_service.get_favorite_subtitle_text_list(
        YouTubeLanguage(language_code), user_id)

    # JSONレスポンスを作成
    data = {
        "favorite_subtitle_list": favorite_subtitle_list
    }

    return JsonResponse(data=data, status=200)


# 指定されたユーザーのベース言語のリストを取得するAPI
@api_view(['GET'])
def get_base_language_list(request):
    user_id = request.user_id
    language_service = LearningLanguageService()

    base_language_list = language_service.get_base_language_list(user_id)

    return JsonResponse(data={
        "base_language_list": base_language_list
    }, status=200)


# 指定されたベース言語IDに対応するベース言語と学習言語の詳細を取得するAPI
@api_view(['GET'])
def get_base_language_detail(request, base_language_id):
    language_service = LearningLanguageService()

    base_language_detail = language_service.get_base_language_detail(base_language_id)

    return JsonResponse(data={
        "base_language_detail": base_language_detail
    }, status=200)


# 指定された学習言語IDの詳細を取得するAPI
@api_view(['GET'])
def get_learning_language_detail(request, learning_language_id):
    language_service = LearningLanguageService()

    learning_language_detail = language_service.get_learning_language_detail(learning_language_id)

    return JsonResponse(data={
        "learning_language_detail": learning_language_detail
    }, status=200)


# 新しいベース言語を作成し、関連する学習言語も作成するAPI
@api_view(['POST'])
def create_base_language(request):
    user_id = request.user_id
    language_code = YouTubeLanguage(request.data.get('language_code'))
    documents = request.data.get('documents')
    is_published = request.data.get('is_published', False)
    learning_language_documents = request.data.get('learning_language_documents', '')
    learning_language_explanation = request.data.get('learning_language_explanation', '')
    learning_language_video_id = request.data.get('learning_language_video_id', '')
    learning_language_timestamp_ms = request.data.get('learning_language_timestamp_ms', 0)

    language_service = LearningLanguageService()
    language_service.create_base_language(
        user_id,
        language_code,
        documents,
        is_published,
        learning_language_documents,
        learning_language_explanation,
        learning_language_video_id,
        learning_language_timestamp_ms
    )

    return JsonResponse(data={"status": 0}, status=200)


@api_view(['POST'])
def create_learning_language(request):
    """
    新しい学習言語を作成するAPI
    """
    base_language_id = request.data.get('base_language_id')
    language_code = request.data.get('language_code')
    documents = request.data.get('documents')
    explanation = request.data.get('explanation')
    video_id = request.data.get('video_id')
    timestamp_ms = request.data.get('timestamp_ms')

    language_service = LearningLanguageService()
    language_service.create_learning_language(
        base_language_id,
        language_code,
        documents,
        explanation,
        video_id,
        timestamp_ms
    )

    return JsonResponse(data={"status": 0}, status=200)


# 指定されたベース言語を更新するAPI
@api_view(['PUT'])
def update_base_language(request, base_language_id):
    documents = request.data.get('documents')
    is_published = request.data.get('is_published')

    language_service = LearningLanguageService()
    language_service.update_base_language(base_language_id, documents, is_published)

    return JsonResponse(data={"status": 0}, status=200)


# 指定された学習言語を更新するAPI
@api_view(['PUT'])
def update_learning_language(request, learning_language_id):
    documents = request.data.get('documents')
    explanation = request.data.get('explanation')
    video_id = request.data.get('video_id')
    timestamp_ms = request.data.get('timestamp_ms')

    language_service = LearningLanguageService()
    language_service.update_learning_language(
        learning_language_id,
        documents,
        explanation,
        video_id,
        timestamp_ms
    )

    return JsonResponse(data={"status": 0}, status=200)


# 指定されたベース言語を削除するAPI
@api_view(['DELETE'])
def delete_base_language(request, base_language_id):
    language_service = LearningLanguageService()
    language_service.delete_base_language(base_language_id)

    return JsonResponse(data={"status": 0}, status=200)


# 指定された学習言語を削除するAPI
@api_view(['DELETE'])
def delete_learning_language(request, learning_language_id):
    language_service = LearningLanguageService()
    language_service.delete_learning_language(learning_language_id)

    return JsonResponse(data={"status": 0}, status=200)
