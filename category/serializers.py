from rest_framework import serializers

from .models import Category


class CategoryTagsSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    @staticmethod
    def get_tags(category_id: int):
        return Category.objects.get(id=category_id).name

    class Meta:
        model = Category
        fields = ("id", "name")


class CategorySerializer(serializers.ModelSerializer):
    # software_set = serializers.ListField(allow_null=True, allow_empty=True)
    # software_set_count = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Category
        fields = ("id", "name")


class CommonResponseSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    msg = serializers.CharField(allow_null=True, allow_blank=True)
    data = serializers.ListField(allow_null=True, allow_empty=True) or serializers.DictField(
        allow_null=True, allow_empty=True
    )
    # data = serializers.DictField(allow_null=True, allow_empty=True)
