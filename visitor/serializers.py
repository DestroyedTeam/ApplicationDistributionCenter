from rest_framework import serializers

from visitor.models import Visitor


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, help_text="用户ID", label="用户ID", required=False, allow_null=True)

    class Meta:
        model = Visitor
        fields = ["id", "username", "head_icon", "role"]
