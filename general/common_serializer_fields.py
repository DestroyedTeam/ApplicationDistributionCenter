from rest_framework import serializers


class DictOrListField(serializers.Field):
    def to_representation(self, value):
        # 这里处理从模型到序列化数据的转换
        if isinstance(value, dict):
            return value
        elif isinstance(value, list):
            return value
        raise serializers.ValidationError("This field must be a dict or list.")

    def to_internal_value(self, data):
        # 这里处理从输入数据到模型数据的转换
        if isinstance(data, dict):
            return data
        elif isinstance(data, list):
            return data
        raise serializers.ValidationError("This field must be a dict or list.")
