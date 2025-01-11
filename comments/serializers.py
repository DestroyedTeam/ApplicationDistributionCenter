from datetime import datetime

from rest_framework import serializers

from articles.serializers import ArticleSerializer
from common.encrypt_schema import EncryptIV
from general.encrypt import encrypt
from software.serializers import SoftwareSerializer
from visitor.serializers import UserSerializer

from .models import Comment


class ArticleTitleSerializer(ArticleSerializer):
    class Meta(ArticleSerializer.Meta):
        fields = ["id", "title"]


class SoftwareNameSerializer(SoftwareSerializer):
    class Meta(SoftwareSerializer.Meta):
        fields = ["id", "name"]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    correlation_article = ArticleTitleSerializer(read_only=True, allow_null=True)
    correlation_software = SoftwareNameSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Comment
        fields = "__all__"

    def to_representation(self, instance):
        """
        重写 to_representation 方法，处理字段加密以及格式化日期
        """
        # 获取父类的序列化结果
        representation = super().to_representation(instance)

        # 加密 'id' 字段
        if "id" in representation:
            representation["id"] = encrypt(representation["id"], iv=EncryptIV.comments.value)
        if representation.get("parent"):
            representation["parent"] = encrypt(representation["parent"], iv=EncryptIV.comments.value)

        # 对关联对象的 id 进行加密
        if representation.get("user"):
            representation["user"]["id"] = encrypt(representation["user"]["id"], iv=EncryptIV.user.value)

        if representation.get("correlation_article"):
            representation["correlation_article"]["id"] = encrypt(
                representation["correlation_article"]["id"], iv=EncryptIV.articles.value
            )

        if representation.get("correlation_software"):
            representation["correlation_software"]["id"] = encrypt(
                representation["correlation_software"]["id"], iv=EncryptIV.software.value
            )

        # 格式化 'created_time' 字段 (假设是发表日期)
        if representation.get("created_time"):
            created_time = representation["created_time"]
            if isinstance(created_time, str):  # 如果是字符串形式的日期
                # 如果是 ISO 格式，先转为 datetime
                created_time = datetime.fromisoformat(created_time)
            # 格式化日期为 "年/月/日 时:分:秒 时区"
            representation["created_time"] = created_time.strftime("%Y/%m/%d %H:%M:%S %z")

        return representation
