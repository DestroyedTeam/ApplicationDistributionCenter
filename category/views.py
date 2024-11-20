# Create your views here.

from django.http import JsonResponse
from rest_framework.views import APIView

from general.common_exceptions import SecurityError
from general.encrypt import decrypt
from general.init_cache import get_all_category

from .serializers import CategorySerializer, CategoryTagsSerializer, CommonResponseSerializer


class Category(APIView):
    def __init__(self):
        super().__init__()
        self.serializer = CommonResponseSerializer

    def get(self, request):
        categories = get_all_category()
        category_id = request.GET.get("category_id")
        if category_id:
            try:
                category_id = category_id.replace(" ", "+")
                category_id = int(decrypt(category_id))
            except ValueError:
                serializer = self.serializer(data={"code": 400, "msg": "invalid category_id", "data": None})
                if serializer.is_valid():
                    return JsonResponse(serializer.data)
                return JsonResponse(serializer.errors)
            except TypeError:
                serializer = self.serializer(data={"code": 400, "msg": "wrong type of category_id", "data": None})
                if serializer.is_valid():
                    return JsonResponse(serializer.data)
                return JsonResponse(serializer.errors)
            except SecurityError as e:
                serializer = self.serializer(data={"code": 400, "msg": str(e), "data": None})
                if serializer.is_valid():
                    return JsonResponse(serializer.data)
                return JsonResponse(serializer.errors)
            except Exception as e:
                serializer = self.serializer(data={"code": 500, "msg": str(e), "data": None})
                if serializer.is_valid():
                    return JsonResponse(serializer.data)
                return JsonResponse(serializer.errors)
            categories = [cate for cate in categories if cate.id == category_id]
        if len(categories) > 0:
            category_serializer = CategorySerializer(data=[category.__dict__ for category in categories], many=True)
            if not category_serializer.is_valid():
                serializer = self.serializer(
                    data={"code": 500, "msg": "序列化失败", "data": category_serializer.errors}
                )
                if serializer.is_valid():
                    return JsonResponse(serializer.data)
                return JsonResponse(serializer.errors)
            serializer = self.serializer(
                data={
                    "code": 200,
                    "msg": "获取成功",
                    "data": [
                        {
                            "category": category,
                            "software_set": category.software_set.all().filter(state=2)[:9],
                            "software_set_count": category.software_set.all().filter(state=2).count(),
                        }
                        for category in categories
                    ],
                }
            )
            if serializer.is_valid():
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors)
        else:
            serializer = self.serializer(data={"code": 404, "msg": "分类（列表）未找到", "data": None})
            if serializer.is_valid():
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors)


class CategoryTags(APIView):
    def __init__(self):
        super().__init__()
        self.serializer = CommonResponseSerializer

    def get(self, request):
        category_id = request.GET.get("category_id")
        if not category_id:
            serializer = self.serializer(data={"code": 400, "msg": "分类ID为空", "data": None})
            if serializer.is_valid():
                return JsonResponse(serializer.data)
            else:
                return JsonResponse(serializer.errors)
        try:
            category_id = int(decrypt(category_id))
            if category_id <= 0:
                serializer = self.serializer(data={"code": 400, "msg": "无效的分类ID", "data": None})
                if serializer.is_valid():
                    return JsonResponse(serializer.data)
                else:
                    return JsonResponse(serializer.errors)
            category_tags_serializer = CategoryTagsSerializer(
                data=CategoryTagsSerializer.get_tags(category_id=category_id)
            )
            if category_tags_serializer.is_valid():
                category_tags = category_tags_serializer.data
                return self.serializer(data={"code": 200, "msg": "获取成功", "data": category_tags}).data
            else:
                return JsonResponse(category_tags_serializer.errors)
        except SecurityError as e:
            serializer = self.serializer(data={"code": 400, "msg": str(e), "data": None})
            if serializer.is_valid():
                return JsonResponse(serializer.data)
            else:
                return JsonResponse(serializer.errors)
        except Exception as e:
            serializer = self.serializer(data={"code": 500, "msg": str(e), "data": None})
            if serializer.is_valid():
                return JsonResponse(serializer.data)
            else:
                return JsonResponse(serializer.errors)
