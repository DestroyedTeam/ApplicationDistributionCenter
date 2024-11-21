from rest_framework import serializers

from software.serializers import SoftwareSerializer

from .models import Category


class CategoryTagsSerializer(serializers.ModelSerializer):
    tags = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        model = Category
        fields = ("id", "name", "tags")


class CategorySerializer(serializers.ModelSerializer):
    software_set = serializers.SerializerMethodField()
    software_set_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "icon", "description", "state", "software_set", "software_set_count"]

    @staticmethod
    def get_software_set(obj):
        software_set = obj.software_set.filter(state=2)[:9]
        return SoftwareSerializer(software_set, many=True).data

    @staticmethod
    def get_software_set_count(obj):
        return obj.software_set.filter(state=2).count()


class CommonResponseSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    msg = serializers.CharField(allow_null=True, allow_blank=True)
    data = serializers.ListField(allow_null=True, allow_empty=True)
