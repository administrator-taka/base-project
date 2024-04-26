from rest_framework import serializers

class ThumbnailSerializer(serializers.Serializer):
    url = serializers.CharField()
    width = serializers.IntegerField()
    height = serializers.IntegerField()

class ThumbnailsMapSerializer(serializers.Serializer):
    default = ThumbnailSerializer()
    medium = ThumbnailSerializer()
    high = ThumbnailSerializer()
    standard = ThumbnailSerializer()
    maxres = ThumbnailSerializer()



class LocalizedSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()


class SnippetSerializer(serializers.Serializer):
    publishedAt = serializers.DateTimeField()
    channelId = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    thumbnails = ThumbnailsMapSerializer()
    channelTitle = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())
    categoryId = serializers.CharField()
    liveBroadcastContent = serializers.CharField()
    localized = LocalizedSerializer()
    defaultAudioLanguage = serializers.CharField()


class ItemSerializer(serializers.Serializer):
    kind = serializers.CharField()
    etag = serializers.CharField()
    id = serializers.CharField()
    snippet = SnippetSerializer()


class PageInfoSerializer(serializers.Serializer):
    totalResults = serializers.IntegerField()
    resultsPerPage = serializers.IntegerField()


class YouTubeVideoSerializer(serializers.Serializer):
    kind = serializers.CharField()
    etag = serializers.CharField()
    items = ItemSerializer(many=True)
    pageInfo = PageInfoSerializer()
