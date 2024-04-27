from django.http import JsonResponse
from django.utils.crypto import get_random_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from myapp.applications.application.service.youtube_download_service import YoutubeDownloadService
from myapp.applications.util.code.youtube_language import YouTubeLanguage
from myproject.settings.base import TEST_YOUTUBE_VIDEO_ID


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    youtube_download_service = YoutubeDownloadService()
    video_id = TEST_YOUTUBE_VIDEO_ID
    default_audio_language = YouTubeLanguage.KOREAN
    translation_language = YouTubeLanguage.JAPANESE

    youtube_download_service.download_video_subtitle(video_id, default_audio_language, translation_language)

    return JsonResponse(data={"msg": "pass"}, status=200)


# APIビューを定義
@api_view(['POST'])
def my_view(request):
    # POSTリクエストのデータを取得
    data = request.data
    print(data)

    # idが"3"のTestモデルのインスタンスを取得
    test_instance = Test.objects.get(id="3")

    # パスワードをランダムな文字列に更新
    new_password = get_random_string(length=12)  # 12文字のランダムな文字列を生成
    test_instance.password = new_password
    test_instance.save()

    # 更新後のTestモデルの全レコードをシリアライズして出力
    tests = Test.objects.all()
    serializer = TestSerializer(tests, many=True)
    print(serializer.data)

    # シリアライズされたデータをレスポンスとして返す
    return Response(serializer.data)


from rest_framework.viewsets import ModelViewSet
from myapp.models import Test
from myapp.serializer.test_serializer import TestSerializer


# モデルビューセットを定義
class TestViewSet(ModelViewSet):
    # 全てのTestモデルのクエリセットを取得
    queryset = Test.objects.all()
    # Testモデル用のシリアライザクラスを指定
    serializer_class = TestSerializer
