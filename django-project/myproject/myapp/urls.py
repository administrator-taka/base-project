from django.urls import path, include
from rest_framework.routers import DefaultRouter

from myapp.views.channel_view import get_channel_data, search_word, download_channel_subtitles, \
    update_translation_language, get_channel_video_list, get_channel_list, search_multiple_word, calculate_channel_word, \
    update_channel_subtitles
from myapp.views.learning_language_view import get_learning_subtitle_text_list, get_favorite_subtitle_text_list, \
    create_base_language, get_base_language_list, get_base_language_detail, update_base_language, delete_base_language, \
    get_learning_language_detail, update_learning_language, delete_learning_language, create_learning_language
from myapp.views.subtitle_text_view import get_subtitle_text_data, update_subtitle_translation, \
    insert_or_update_subtitle_learning_memory, execute_chatgpt_translation
from myapp.views.test_views import TestViewSet
from myapp.views.video_view import get_video_data, download_video_subtitle

# デフォルトのルーターを作成
router = DefaultRouter()

# TestViewSetをルーターに登録
router.register(r'test', TestViewSet)

# APIのルートURLを設定
urlpatterns = [
    path('', include(router.urls)),  # 空の文字列にルーターのURLを含めます
    path("channel", get_channel_list, name="get_channel_list"),
    path("channel/<str:channel_id>", get_channel_data, name="get_channel_data"),
    path("channel/<str:channel_id>/calculate_channel_word", calculate_channel_word, name="calculate_channel_word"),
    path("channel/<str:channel_id>/get_channel_video_list", get_channel_video_list, name="get_channel_video_list"),
    path("channel/<str:channel_id>/download_channel_subtitles", download_channel_subtitles,
         name="download_channel_subtitles"),
    path("channel/<str:channel_id>/search_word", search_word, name="search_word"),
    path("channel/<str:channel_id>/search_multiple_word", search_multiple_word, name="search_multiple_word"),
    path("channel/<str:channel_id>/update_translation_language", update_translation_language,
         name="update_translation_language"),
    path("channel/<str:channel_id>/update_channel_subtitles", update_channel_subtitles,
         name="update_channel_subtitles"),
    path("video/<str:video_id>", get_video_data, name="get_video_data"),
    path("video/<str:video_id>/download_video_subtitle", download_video_subtitle, name="download_video_subtitle"),
    path("subtitle/<str:subtitle_text_id>", get_subtitle_text_data, name="get_subtitle_text_data"),
    path("subtitle/<str:subtitle_text_id>/execute_chatgpt_translation", execute_chatgpt_translation, name="execute_chatgpt_translation"),
    path("subtitle/<str:subtitle_text_id>/update_subtitle_translation", update_subtitle_translation,
         name="update_subtitle_translation"),
    path("subtitle/<str:subtitle_text_id>/insert_or_update_subtitle_learning_memory",
         insert_or_update_subtitle_learning_memory,
         name="insert_or_update_subtitle_learning_memory"),
    path("learning", get_learning_subtitle_text_list,
         name="get_learning_subtitle_text_list"),
    path("favorite", get_favorite_subtitle_text_list,
         name="get_favorite_subtitle_text_list"),
    # ベース言語に関するエンドポイント
    path("base-language/create", create_base_language, name="create_base_language"),
    path("base-language/list", get_base_language_list, name="get_base_language_list"),
    path("base-language/<str:base_language_id>/detail", get_base_language_detail, name="get_base_language_detail"),
    path("base-language/<str:base_language_id>/update", update_base_language, name="update_base_language"),
    path("base-language/<str:base_language_id>/delete", delete_base_language, name="delete_base_language"),

    # 学習言語に関するエンドポイント
    path("learning-language/create", create_learning_language, name="create_learning_language"),
    path("learning-language/<str:learning_language_id>/detail", get_learning_language_detail,
         name="get_learning_language_detail"),
    path("learning-language/<str:learning_language_id>/update", update_learning_language,
         name="update_learning_language"),
    path("learning-language/<str:learning_language_id>/delete", delete_learning_language,
         name="delete_learning_language"),
]