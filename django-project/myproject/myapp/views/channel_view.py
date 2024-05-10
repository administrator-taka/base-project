from django.http import JsonResponse
from rest_framework.decorators import api_view

from myapp.applications.application.service.youtube_download_service import YoutubeDownloadService
from myapp.applications.util.code.subtitle_type import SubtitleType


@api_view(['GET'])
def get_channel_data(request, channel_id):
    youtube_download_service = YoutubeDownloadService()
    channel_data = youtube_download_service.get_channel_data(channel_id)
    response = youtube_download_service.get_channel_subtitle_list(channel_id)
    # JSONレスポンスを作成
    data = {
        "channel_data": channel_data,
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


@api_view(['POST'])
def update_translation_language(request, channel_id):
    # リクエストのJSONの中身を取得
    request_data = request.data

    default_audio_language = request_data.get('default_audio_language', None)
    translation_languages = request_data.get('translation_languages', None)

    youtube_download_service = YoutubeDownloadService()

    youtube_download_service.update_channel_translation_info(channel_id, default_audio_language, translation_languages)

    # JSONレスポンスを作成
    data = {
        "response": "response"
    }

    return JsonResponse(data=data, status=200)
