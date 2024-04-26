from rest_framework import serializers


class SegSerializer(serializers.Serializer):
    utf8 = serializers.CharField(required=False, default='')


class EventSerializer(serializers.Serializer):
    tStartMs = serializers.IntegerField(required=False, default=0)
    dDurationMs = serializers.IntegerField(required=False, default=0)
    segs = SegSerializer(many=True)


class YouTubeSubtitleSerializer(serializers.Serializer):
    events = EventSerializer(many=True)


def process_result(result_json):
    serializer = YouTubeSubtitleSerializer(data=result_json)
    if serializer.is_valid():
        return serializer.data
    else:
        return serializer.errors
