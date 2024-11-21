from rest_framework import serializers


class CommonResponseSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    msg = serializers.CharField(allow_null=True, allow_blank=True)
    data = serializers.ListField(allow_null=True, allow_empty=True, default=[])
