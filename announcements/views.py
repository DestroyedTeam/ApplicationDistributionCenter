# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import APIView

from announcements.serializers import NoticesSerializer
from general.encrypt import decrypt, encrypt
from general.init_cache import get_notices


class Notices(APIView):
    def __init__(self):
        super().__init__()
        self.serializer = NoticesSerializer

    def get(self, request):
        software_id = request.GET.get("software_id")
        if software_id:
            try:
                software_id = decrypt(software_id.replace(" ", "+"))
                software_id = int(software_id)
            except Exception:
                serializer = self.serializer(data={"code": 400, "msg": "参数错误"})
                serializer.is_valid(raise_exception=True)
                return JsonResponse(serializer.data)
            notices = get_notices(software_id=software_id)
        else:
            notices = get_notices()
            notices = [notice for notice in notices if notice.type == 1]

        notices = [
            {
                "id": str(encrypt(str(notice.id))) if software_id else notice.id,
                "title": notice.title,
                "content": notice.content,
                "created_time": notice.created_time,
                "image": notice.image.url if notice.image else None,
                "app": notice.app.name if software_id and notice.app else None,
            }
            for notice in notices
        ]
        try:
            serializer = self.serializer(data={"code": 200, "msg": "获取成功", "data": notices})
            if not notices or len(notices) == 0:
                serializer = self.serializer(data={"code": 204, "msg": "请求成功但无数据", "data": notices})
            serializer.is_valid(raise_exception=True)
            return JsonResponse(serializer.data)
        except Exception:
            serializer = self.serializer(data={"code": 500, "msg": "服务器错误"})
            serializer.is_valid(raise_exception=True)
            return JsonResponse(serializer.data)
