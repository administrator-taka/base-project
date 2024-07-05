from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from myapp.applications.application.service.channel_service import ChannelService


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    youtube_download_service = ChannelService()
    channel_id = ''
    youtube_download_service.delete_channel_data(channel_id)
    return JsonResponse(data={"msg": "pass"}, status=200)
