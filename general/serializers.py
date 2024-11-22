from rest_framework import serializers

from general.common_serializer_fields import DictOrListField


class CommonResponseSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    msg = serializers.CharField(allow_null=True, allow_blank=True)
    data = DictOrListField(allow_null=True, default=None)
