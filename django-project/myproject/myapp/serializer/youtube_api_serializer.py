from rest_framework import serializers


class ThumbnailSerializer(serializers.Serializer):
    url = serializers.CharField(required=False, default='')
    width = serializers.IntegerField(required=False, default=0)
    height = serializers.IntegerField(required=False, default=0)


class ThumbnailsMapSerializer(serializers.Serializer):
    default = ThumbnailSerializer(required=False, default={})
    medium = ThumbnailSerializer(required=False, default={})
    high = ThumbnailSerializer(required=False, default={})
    standard = ThumbnailSerializer(required=False, default={})
    maxres = ThumbnailSerializer(required=False, default={})


class LocalizedSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, default='')
    description = serializers.CharField(required=False, default='')


class SnippetSerializer(serializers.Serializer):
    publishedAt = serializers.DateTimeField(required=False, default=None)
    channelId = serializers.CharField(required=False, default='')
    title = serializers.CharField(required=False, default='')
    description = serializers.CharField(required=False, default='')
    thumbnails = ThumbnailsMapSerializer(required=False, default={})
    channelTitle = serializers.CharField(required=False, default='')
    tags = serializers.ListField(child=serializers.CharField(), required=False, default=[])
    categoryId = serializers.CharField(required=False, default='')
    liveBroadcastContent = serializers.CharField(required=False, default='')
    localized = LocalizedSerializer(required=False, default={})
    defaultAudioLanguage = serializers.CharField(required=False, default='')


class LiveStreamingDetailsSerializer(serializers.Serializer):
    actualStartTime = serializers.DateTimeField(required=False, default=None)
    actualEndTime = serializers.DateTimeField(required=False, default=None)
    scheduledStartTime = serializers.DateTimeField(required=False, default=None)
    scheduledEndTime = serializers.DateTimeField(required=False, default=None)
    concurrentViewers = serializers.IntegerField(required=False, default=0)
    activeLiveChatId = serializers.CharField(required=False, default='')


class LocalizedTextSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, default='')
    description = serializers.CharField(required=False, default='')


class LocalizationsSerializer(serializers.DictField):
    child = LocalizedTextSerializer()


class ItemSerializer(serializers.Serializer):
    kind = serializers.CharField(required=False, default='')
    etag = serializers.CharField(required=False, default='')
    id = serializers.CharField(required=False, default='')
    snippet = SnippetSerializer(required=False, default={})
    liveStreamingDetails = LiveStreamingDetailsSerializer()
    localizations = LocalizationsSerializer(required=False, default={})


class PageInfoSerializer(serializers.Serializer):
    totalResults = serializers.IntegerField(required=False, default=0)
    resultsPerPage = serializers.IntegerField(required=False, default=0)


class YouTubeVideoSerializer(serializers.Serializer):
    kind = serializers.CharField(required=False, default='')
    etag = serializers.CharField(required=False, default='')
    items = ItemSerializer(many=True, required=False, default=[])
    pageInfo = PageInfoSerializer(required=False, default={})
