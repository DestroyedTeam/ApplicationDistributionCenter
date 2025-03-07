from rest_framework import serializers

from .models import SoftWare


class SoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftWare
        fields = [
            "id",
            "name",
            "version",
            "language",
            "platform",
            "run_os_version",
            "description",
            "category",
            "tags",
            "file_size",
            "official_link",
            "link_adrive",
            "link_baidu",
            "link_direct",
            "link_123",
            "icon",
            "state",
            "user",
            "view_volume",
            "thumbs_volume",
            "download_volume",
            "created_time",
            "updated_time",
        ]
