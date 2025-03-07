from rest_framework import serializers

from software.serializers import SoftwareSerializer
from visitor.serializers import UserSerializer

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    cover = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    correlation_software = SoftwareSerializer(read_only=True, allow_null=True)

    def create(self, validated_data):
        """
        当调用ArticleSerializer实例.save()时，会调用此方法
        """
        if "cover" not in validated_data or validated_data["cover"] is None:
            validated_data["cover"] = "article/default.png"
        return super().create(validated_data)

    class Meta:
        """
        由于Article模型中的cover字段有默认值，所以在序列化时不需要指定cover字段，
        此处如果强制指定cover字段，会导致ArticleSerializer序列化失败（校验无法通过）
        因为Article模型中的cover字段是ImageField类型，但是在序列化时，一般情况下不会直接传bytes类型来做检查
        只是传入文件路径即可，所以在序列化时，不需要指定cover字段
        """

        model = Article
        fields = ["user", "title", "content", "cover", "correlation_software"]
        read_only_fields = ["id", "view_volume", "thumbs_volume", "created_time", "updated_time"]


class ArticleDetailSerializer(serializers.ModelSerializer):
    """
    用于文章详情页/文章详细信息API的序列化
    """

    user = UserSerializer(read_only=True)
    correlation_software = SoftwareSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ["id", "view_volume", "thumbs_volume", "created_time", "updated_time"]
