from django.urls import path, include
from rest_framework.routers import DefaultRouter

from myapp.views.channel_view import get_channel_data, search_word, download_channel_subtitles, \
    update_translation_language
from myapp.views.test_views import TestViewSet
from myapp.views.video_view import get_video_data

# デフォルトのルーターを作成
router = DefaultRouter()

# TestViewSetをルーターに登録
router.register(r'test', TestViewSet)

# APIのルートURLを設定
urlpatterns = [
    path('', include(router.urls)),  # 空の文字列にルーターのURLを含めます
    path("channel/<str:channel_id>/", get_channel_data, name="get_channel_data"),
    path("channel/<str:channel_id>/download_channel_subtitles", download_channel_subtitles,
         name="download_channel_subtitles"),
    path("channel/<str:channel_id>/search_word", search_word, name="search_word"),
    path("channel/<str:channel_id>/update_translation_language", update_translation_language, name="update_translation_language"),
    path("video/<str:video_id>/", get_video_data, name="get_video_data"),
]
