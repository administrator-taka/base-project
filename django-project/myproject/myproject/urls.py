from django.contrib import admin
from django.urls import path, include

from myapp.views.health_check_view import health_check
from myapp.views.test_views import my_view

urlpatterns = [
    path('admin/', admin.site.urls),  # adminパネルへのURL
    path('api/', my_view, name='my-view'),  # '/api/'へのリクエストをmy_view関数にルーティングし、'my-view'という名前を付けます
    # path('db/', include('myapp.urls')),  # '/db/'へのリクエストをmyappアプリケーションのURL設定に含まれるものにルーティングします
    path("health/", health_check, name="health"),

    path('youtube_app/', include('myapp.urls')),  # channelごとの処理

]
