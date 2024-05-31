import time
from datetime import datetime

from django.http import JsonResponse
from rest_framework.decorators import api_view

from myapp.applications.application.service.youtube_download_service import YoutubeDownloadService
from myapp.applications.util.code.subtitle_type import SubtitleType
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myapp.applications.util.file_handler import FileHandler
from myapp.applications.util.util_convert import milliseconds_to_timestamp


@api_view(['GET'])
def get_channel_list(request):
    youtube_download_service = YoutubeDownloadService()
    channel_list = youtube_download_service.get_activate_channel_list()
    # JSONレスポンスを作成
    data = {
        "channel_list": channel_list,
    }

    return JsonResponse(data=data, status=200)


@api_view(['GET'])
def get_channel_data(request, channel_id):
    youtube_download_service = YoutubeDownloadService()
    channel_data = youtube_download_service.get_channel_data(channel_id)
    # JSONレスポンスを作成
    data = {
        "channel_data": channel_data,
    }

    return JsonResponse(data=data, status=200)


@api_view(['POST'])
def get_channel_video_list(request, channel_id):
    youtube_download_service = YoutubeDownloadService()
    languages = [YouTubeLanguage(language) for language in request.data.get('languages', [])]

    page = request.data.get('page', 1)
    page_size = request.data.get('page_size', 10)
    results = youtube_download_service.get_channel_subtitle_list(channel_id, languages, page, page_size)

    # JSONレスポンスを作成
    data = {
        "results": results,
    }

    return JsonResponse(data=data, status=200)



@api_view(['GET'])
def download_channel_subtitles(request, channel_id):
    start_time = time.time()
    start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    youtube_download_service = YoutubeDownloadService()
    youtube_download_service.download_channel_subtitles(channel_id)

    end_time = time.time()
    end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 処理時間を計算
    elapsed_time = end_time - start_time

    # JSONレスポンスを作成
    data = {
        "start_time": start_datetime,
        "end_time": end_datetime,
        "elapsed_time": milliseconds_to_timestamp(int(elapsed_time * 1000))
    }

    # チャンネルIDを含むファイル名を生成
    file_name = f"download_channel_subtitles_{channel_id}"

    # JSONレスポンスをファイルに書き込む
    FileHandler.write_json_response(data, file_name=file_name)

    return JsonResponse(data=data, status=200)


@api_view(['POST'])
def search_word(request, channel_id):
    # リクエストのJSONの中身を取得
    request_data = request.data

    # search_wordを取得
    search_word = request_data.get('search_word', None)

    # search_wordが空文字、空白、またはNoneの場合、処理を中断しエラーレスポンスを返す
    if not search_word or search_word.strip() == '':
        # TODO:バリデーション、エラーレスポンス追加
        return JsonResponse(data={'error': '検索ワードが無効です。'}, status=400)

    youtube_download_service = YoutubeDownloadService()
    # TODO:言語どうにかする
    search_results = youtube_download_service.search_single_row_word(search_word, channel_id, SubtitleType.MANUAL)
    # JSONレスポンスを作成
    data = {
        "search_results": search_results
    }

    return JsonResponse(data=data, status=200)


@api_view(['POST'])
def update_translation_language(request, channel_id):
    # リクエストのJSONの中身を取得
    request_data = request.data

    # デフォルトの言語コードを取得
    default_audio_language = YouTubeLanguage(request_data.get('default_audio_language', None))

    # 翻訳言語リスト取得
    translation_languages = [YouTubeLanguage(language) for language in request_data.get('translation_languages', None)]

    youtube_download_service = YoutubeDownloadService()

    youtube_download_service.update_channel_translation_info(channel_id, default_audio_language, translation_languages)

    youtube_download_service.insert_initial_video_data(channel_id)

    # JSONレスポンスを作成
    data = {
        "status": 0
    }

    return JsonResponse(data=data, status=200)
