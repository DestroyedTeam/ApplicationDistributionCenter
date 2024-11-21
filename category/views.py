# Create your views here.

from django.http import JsonResponse
from rest_framework.views import APIView

from general.common_exceptions import SecurityError
from general.encrypt import decrypt
from general.init_cache import get_all_category

from .models import Category
from .serializers import CategorySerializer, CategoryTagsSerializer, CommonResponseSerializer


class CategoryView(APIView):
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
            categories = categories.filter(id=category_id)

        # 格式化categories_data,将software_set和software_set_count添加到categories_data中
        if len(categories) > 0:
            category_serializer = CategorySerializer(categories, many=True)
            serializer = self.serializer(
                data={
                    "code": 200,
                    "msg": "获取成功",
                    "data": category_serializer.data,
                }
            )
            if serializer.is_valid():
                return JsonResponse({"categories": serializer.data})
            return JsonResponse(serializer.errors)
        else:
            serializer = self.serializer(data={"code": 404, "msg": "分类（列表）未找到", "data": None})
            if serializer.is_valid():
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors)


class CategoryTagsView(APIView):
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
            category = Category.objects.get(id=category_id)
            category.tags = category.slug
            # TODO: 当前版本,标签已从分类中分离,此处应该返回分类的标签
            category_tags_serializer = CategoryTagsSerializer(category)
            serializer = self.serializer(data={"code": 200, "msg": "获取成功", "data": [category_tags_serializer.data]})
            if serializer.is_valid():
                return JsonResponse(serializer.data)
            else:
                return JsonResponse(serializer.errors)
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
