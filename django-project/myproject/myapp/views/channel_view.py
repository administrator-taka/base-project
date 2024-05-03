from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from myapp.applications.application.service.youtube_download_service import YoutubeDownloadService
from myapp.applications.util.code.subtitle_type import SubtitleType
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myproject.settings.base import TEST_YOUTUBE_VIDEO_ID, TEST_YOUTUBE_CHANNEL_ID


@api_view(['GET'])
def get_channel_data(request, channel_id):
    youtube_download_service = YoutubeDownloadService()
    # TODO:channel_dataのinsertと取得
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


def test_1():
    youtube_download_service = YoutubeDownloadService()
    video_id = TEST_YOUTUBE_VIDEO_ID
    default_audio_language = YouTubeLanguage.KOREAN
    translation_language = YouTubeLanguage.JAPANESE

    youtube_download_service.download_video_subtitle(video_id, default_audio_language, translation_language)


def test_2():
    # 全部の字幕データを取得する動作確認用
    youtube_download_service = YoutubeDownloadService()

    channel_id = TEST_YOUTUBE_CHANNEL_ID

    youtube_download_service.download_channel_subtitles(channel_id)


def test_3():
    youtube_download_service = YoutubeDownloadService()
    video_id = TEST_YOUTUBE_VIDEO_ID
    youtube_download_service.insert_initial_subtitle_detail(video_id)


def test_4():
    youtube_download_service = YoutubeDownloadService()
    channel_id = TEST_YOUTUBE_CHANNEL_ID
    youtube_download_service.get_channel_subtitle_list(channel_id)


def test_5():
    youtube_download_service = YoutubeDownloadService()
    channel_id = TEST_YOUTUBE_CHANNEL_ID
    youtube_download_service.insert_initial_video_data(channel_id)


def test_6():
    youtube_download_service = YoutubeDownloadService()
    youtube_download_service.search_single_row_word("미안해", TEST_YOUTUBE_CHANNEL_ID, SubtitleType.MANUAL,
                                                    YouTubeLanguage.KOREAN)
