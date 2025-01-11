# Create your views here.

from django.http import JsonResponse
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from comments.serializers import CommentSerializer
from common.encrypt_schema import EncryptIV
from common.log_schema import LogType
from general.encrypt import decrypt
from general.init_cache import get_articles, get_comments, get_software
from general.serializers import CommonResponseSerializer
from utils.fields_filter import filter_empty_string
from utils.logger import logger
from visitor.models import Visitor


class CommentView(APIView):
    def __init__(self):
        super().__init__()
        self.serializer = CommonResponseSerializer

    @staticmethod
    def _log(
        msg: str, data: dict, log_type: LogType = LogType.ERROR, serializer: type(Serializer) = CommonResponseSerializer
    ):
        logger.log(level=log_type.value, message=msg)
        response_serializer = serializer(data=data)
        return (
            JsonResponse(response_serializer.data, status=data.get("code"))
            if response_serializer.is_valid()
            else JsonResponse(response_serializer.errors, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        )

    def get(self, request):
        # 校验请求参数
        try:
            query_id, comment_type, page, page_size = filter_empty_string(
                request.GET.get("query_id"),
                request.GET.get("comment_type"),
                request.GET.get("page"),
                request.GET.get("page_size"),
            )
            decrypt_iv = EncryptIV.articles.value if comment_type == "article" else EncryptIV.software.value
            query_id = int(decrypt(query_id, iv=decrypt_iv))
            page, page_size = int(page), int(page_size)
        except Exception as e:
            return self._log(
                f"Error during parse request params: {e}",
                {"code": status.HTTP_428_PRECONDITION_REQUIRED, "msg": "failed with invalid params"},
            )

        comments = (
            get_comments(software_id=query_id, page=page, page_size=page_size)
            if comment_type == "software"
            else get_comments(article_id=query_id, page=page, page_size=page_size)
        )

        if len(comments) <= 0:
            return self._log(
                "Not Found any comments",
                {"code": status.HTTP_404_NOT_FOUND, "msg": "Not Found any comments"},
                LogType.WARNING,
            )
        try:
            comment_serializer = CommentSerializer(comments, many=True)
            serializer = self.serializer(
                data={"code": status.HTTP_200_OK, "msg": "success", "data": {"comments": comment_serializer.data}}
            )
            return (
                JsonResponse(serializer.validated_data, status=status.HTTP_200_OK)
                if serializer.is_valid()
                else JsonResponse(serializer.errors, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            )
        except Exception as e:
            return self._log(
                f"Error during serialize comments: {e}",
                {"code": status.HTTP_500_INTERNAL_SERVER_ERROR, "msg": "failed when serialize comments"},
            )

    def post(self, request):
        try:
            # NOTE: Only for test
            user = Visitor.objects.get(id=1)
            # user = Visitor.objects.get(django_user__username=request.user.username) if not request.user.is_anonymous else None
            if not user:
                return self._log(
                    "Failed with unauthorized user",
                    {"code": status.HTTP_401_UNAUTHORIZED, "msg": "failed with unauthorized user"},
                )
            content = filter_empty_string(request.POST.get("comment"))
            if not content:
                return self._log(
                    "Failed with empty comment content",
                    {"code": status.HTTP_400_BAD_REQUEST, "msg": "failed with empty comment content"},
                )
            correlation_article_id = int(decrypt(request.POST.get("article_id"), iv=EncryptIV.articles.value))
            correlation_software_id = int(decrypt(request.POST.get("software_id"), iv=EncryptIV.software.value))
            # parent_id = int(decrypt(request.POST.get("comment_parent"), iv=EncryptIV.comments.value))
        except Exception as e:
            return self._log(
                f"Error during parse request params: {e}",
                {"code": status.HTTP_400_BAD_REQUEST, "msg": "failed with invalid params"},
            )

        correlation_article = get_articles(article_id=correlation_article_id)
        correlation_software = get_software(software_id=correlation_software_id)

        if not correlation_article and not correlation_software:
            return self._log(
                f"Failed with invalid article_id: {correlation_article_id} or software_id: {correlation_software_id}",
                {"code": status.HTTP_400_BAD_REQUEST, "msg": "failed with invalid article_id or software_id"},
            )
        # TODO: 评论的逻辑处理
