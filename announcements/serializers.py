from rest_framework import serializers


class NoticeSerializer(serializers.Serializer):
    id = serializers.CharField(allow_null=True, allow_blank=True)
    title = serializers.CharField(allow_null=True, allow_blank=True)
    content = serializers.CharField(allow_null=True, allow_blank=True)
    created_time = serializers.DateTimeField(allow_null=True)
    image = serializers.URLField(allow_null=True)
    app = serializers.CharField(allow_null=True, allow_blank=True)


class NoticesSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    msg = serializers.CharField()
    data = NoticeSerializer(many=True, allow_null=True)
