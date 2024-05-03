from django.urls import path, include
from rest_framework.routers import DefaultRouter

from myapp.views.channel_view import get_channel_data, search_word
from myapp.views.test_views import TestViewSet

# デフォルトのルーターを作成
router = DefaultRouter()

# TestViewSetをルーターに登録
router.register(r'test', TestViewSet)

# APIのルートURLを設定
urlpatterns = [
    path('', include(router.urls)),  # 空の文字列にルーターのURLを含めます
    path("channel/<str:channel_id>/", get_channel_data, name="get_channel_data"),
    path("channel/<str:channel_id>/search_word", search_word, name="search_word"),  # 新しいビューのパスを追加
]
