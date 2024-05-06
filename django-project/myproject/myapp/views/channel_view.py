from django.http import JsonResponse
from rest_framework.decorators import api_view

from myapp.applications.application.service.youtube_download_service import YoutubeDownloadService
from myapp.applications.util.code.subtitle_type import SubtitleType


@api_view(['GET'])
def get_channel_data(request, channel_id):
    youtube_download_service = YoutubeDownloadService()
    youtube_download_service.insert_channel_data(channel_id)
    response = youtube_download_service.get_channel_subtitle_list(channel_id)
    # JSONレスポンスを作成
    data = {
        "channel_data": None,
        "response": response
    }

    return JsonResponse(data=data, status=200)


@api_view(['GET'])
def download_channel_subtitles(request, channel_id):
    youtube_download_service = YoutubeDownloadService()
    youtube_download_service.download_channel_subtitles(channel_id)

    # JSONレスポンスを作成
    data = {
        # TODO:字幕更新のレスポンスを考える。ページング等も
        "response": "response"
    }

    return JsonResponse(data=data, status=200)


@api_view(['POST'])
def search_word(request, channel_id):
    # リクエストのJSONの中身を取得
    request_data = request.data

    # search_wordを取得
    search_word = request_data.get('search_word', None)

    youtube_download_service = YoutubeDownloadService()
    # TODO:言語どうにかする
    response = youtube_download_service.search_single_row_word(search_word, channel_id, SubtitleType.MANUAL)
    # JSONレスポンスを作成
    data = {
        "response": response
    }

    return JsonResponse(data=data, status=200)


@api_view(['GET'])
def update_translation_language(request, channel_id):
    # JSONレスポンスを作成
    data = {
        "response": "response"
    }

    return JsonResponse(data=data, status=200)
