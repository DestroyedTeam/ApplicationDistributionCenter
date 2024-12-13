# Create your views here.

from django.http import JsonResponse
from django.shortcuts import render
from loguru import logger
from more_itertools.more import raise_
from rest_framework import status
from rest_framework.decorators import APIView

from general.common_compute import compute_similarity, get_related_articles
from general.common_exceptions import SecurityError
from general.data_handler import get_image_urls_from_md_str
from general.encrypt import decrypt
from general.init_cache import get_articles
from general.serializers import CommonResponseSerializer
from software.models import SoftWare
from utils.fields_filter import filter_empty_string
from visitor.models import Visitor

from .enums import ThumbType
from .models import Article
from .serializers import ArticleDetailSerializer, ArticleSerializer
from .utils import UpdateArticleViewVolume


class ArticleAPIView(APIView):
    def __init__(self):
        super().__init__()
        self.serializer = CommonResponseSerializer

    @staticmethod
    @UpdateArticleViewVolume
    def get(request):
        # id参数获取及校验
        article_id = request.GET.get("article_id")
        try:
            article_id = decrypt(article_id) if article_id else None
        except SecurityError:
            serializer = CommonResponseSerializer(
                data={"code": status.HTTP_400_BAD_REQUEST, "msg": "failed with decrypt params"}
            )
            return (
                JsonResponse(serializer.data) if serializer.is_valid() else JsonResponse(serializer.errors, safe=False)
            )
        except Exception:
            serializer = CommonResponseSerializer(
                data={"code": status.HTTP_400_BAD_REQUEST, "msg": "failed with invalid params"}
            )
            return (
                JsonResponse(serializer.data) if serializer.is_valid() else JsonResponse(serializer.errors, safe=False)
            )

        articles = get_articles() if not article_id else get_articles(article_id=article_id)

        # 页面参数获取及校验
        try:
            if (not article_id) and request.GET.get("page"):
                page_num = int(request.GET.get("page"))
            else:
                page_num = -1
        except Exception:
            serializer = CommonResponseSerializer(
                data={"code": status.HTTP_400_BAD_REQUEST, "msg": "failed with invalid params"}
            )
            return (
                JsonResponse(serializer.data) if serializer.is_valid() else JsonResponse(serializer.errors, safe=False)
            )
        if page_num and page_num > 0:
            page_num -= 1
            articles = articles.filter()[page_num * 6 : page_num * 6 + 6]

        if articles and len(articles) > 0:
            article_serializer = (
                ArticleSerializer(articles, many=True)
                if not article_id
                else ArticleDetailSerializer(articles, many=True)
            )
            if not article_serializer.data and not article_id:
                serializer = CommonResponseSerializer(
                    data={"code": status.HTTP_400_BAD_REQUEST, "msg": "failed with invalid data"}
                )
                return (
                    JsonResponse(serializer.data)
                    if serializer.is_valid()
                    else JsonResponse(serializer.errors, safe=False)
                )
            # 获取到数据后返回
            serializer = CommonResponseSerializer(
                data={"code": status.HTTP_200_OK, "msg": "success", "data": article_serializer.data}
            )
            return (
                JsonResponse(serializer.data) if serializer.is_valid() else JsonResponse(serializer.errors, safe=False)
            )
        else:
            # 无数据返回
            serializer = CommonResponseSerializer(data={"code": status.HTTP_204_NO_CONTENT, "msg": "获取成功但空数据"})
            return (
                JsonResponse(serializer.data) if serializer.is_valid() else JsonResponse(serializer.errors, safe=False)
            )

    def post(self, request):
        """
        发表文章
        """
        try:
            # NOTE:仅供测试使用
            # user = Visitor.objects.get(id=1)
            user = (
                Visitor.objects.get(django_user__username=request.user.username)
                if not request.user.is_anonymous
                else None
            )
            if not user:
                serializer = self.serializer(data={"code": status.HTTP_401_UNAUTHORIZED, "msg": "failed with no user"})
                return (
                    JsonResponse(serializer.data)
                    if serializer.is_valid()
                    else JsonResponse(serializer.errors, safe=False)
                )
            title, content = filter_empty_string(request.POST.get("title"), request.POST.get("content"))
            cover = get_image_urls_from_md_str(content)
            if not cover or len(cover) <= 0:
                cover = None
            else:
                cover = [c for c in cover if c.split(".")[-1] in ["jpg", "jpeg", "png", "gif"]]
                if len(cover) > 0:
                    cover = cover[0].replace("/media/", "")
                else:
                    cover = None
            correlation_software_id = filter_empty_string(request.POST.get("correlation_software_id"))
            correlation_software = (
                SoftWare.objects.get(id=decrypt(correlation_software_id)) if correlation_software_id else None
            )

            article_serializer = ArticleSerializer(
                data={
                    "user": user.id,
                    "title": title,
                    "content": content,
                    **{"cover": cover if cover else None},
                    "correlation_software": correlation_software,
                }
            )

            if article_serializer.is_valid():
                article = article_serializer.save()  # 保存文章并返回文章对象
                return_data = {
                    "code": status.HTTP_201_CREATED,
                    "msg": "上传成功",
                    "data": [{"article_id": article.id}],  # 返回文章ID
                }
            else:
                return_data = {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "msg": "上传失败（在序列化文章并保存到数据库时）",
                    "data": article_serializer.errors,
                }
            serializer = self.serializer(data=return_data)
            return (
                JsonResponse(serializer.data) if serializer.is_valid() else JsonResponse(serializer.errors, safe=False)
            )
        except SecurityError:
            serializer = self.serializer(
                data={"code": status.HTTP_400_BAD_REQUEST, "msg": "failed with decrypt params"}
            )
            return (
                JsonResponse(serializer.data) if serializer.is_valid() else JsonResponse(serializer.errors, safe=False)
            )
        except Exception as e:
            logger.error(f"failed with `{e}` in publish article")
            serializer = self.serializer(data={"code": status.HTTP_400_BAD_REQUEST, "msg": "failed in publish article"})
            return (
                JsonResponse(serializer.data) if serializer.is_valid() else JsonResponse(serializer.errors, safe=False)
            )

    def put(self, request):
        pass

    def delete(self, request):
        pass


class ArticlePageView(APIView):
    @staticmethod
    @UpdateArticleViewVolume
    def get(request):
        article_id = request.GET.get("article_id")
        try:
            article_id = decrypt(article_id) if article_id else None
        except SecurityError:
            return render(request, "article_details.html", {"error": "解析ID失败", "code": status.HTTP_400_BAD_REQUEST})
        except Exception:
            return render(request, "article_details.html", {"error": "无效参数", "code": status.HTTP_400_BAD_REQUEST})
        articles = get_articles().filter()[:6] if not article_id else get_articles(article_id=article_id).filter()
        serializer = ArticleSerializer(articles, many=True)
        if serializer.data:
            if article_id:
                related_articles = [article for article in articles if article.id != article_id]
                related_articles = sorted(
                    related_articles,
                    key=lambda x: compute_similarity(articles[0].plain_content(), x.plain_content()),
                    reverse=True,
                )[:6]
                related_software = [
                    article.correlation_software
                    for article in articles
                    if article.id == article_id and article.correlation_software
                ]
                context_articles = get_related_articles(articles, article_id)
                artile_detail = {
                    "article": articles[0],
                    "context_articles": context_articles,
                    "related_articles": related_articles,
                    "related_software": related_software,
                    "respond_comment": "article",
                }
                return render(request, "article_details.html", artile_detail)

            articles_count = get_articles().count()
            return render(request, "articles_list.html", {"articles": articles, "articles_count": articles_count})
        return render(
            request, "articles_list.html", {"error": "序列化失败或未找到文章", "code": status.HTTP_400_BAD_REQUEST}
        )


class ArticleThumbView(APIView):
    def __init__(self):
        super().__init__()
        self.serializer = CommonResponseSerializer

    def post(self, request):
        try:
            post_data: dict = request.data
            thumb_type, article_id = filter_empty_string(post_data.get("thumb_type"), post_data.get("article_id"))
            article_id = decrypt(article_id) if article_id else raise_(SecurityError)
            article = Article.objects.get(id=article_id)

            def _update_article_thumb(art: Article, thumb: bool = True):
                art.thumbs_volume += 1 if thumb else -1
                if art.thumbs_volume < 0:
                    art.thumbs_volume = 0
                art.save()

            if thumb_type == ThumbType.THUMB.value:
                if article:
                    _update_article_thumb(article)
                    serializer = self.serializer(data={"code": status.HTTP_200_OK, "msg": "点赞成功"})
                    return (
                        JsonResponse(serializer.data)
                        if serializer.is_valid()
                        else JsonResponse(serializer.errors, safe=False)
                    )
                else:
                    logger.error("failed with invalid article")
                    serializer = self.serializer(data={"code": status.HTTP_404_NOT_FOUND, "msg": "未找到文章"})
                    return (
                        JsonResponse(serializer.data)
                        if serializer.is_valid()
                        else JsonResponse(serializer.errors, safe=False)
                    )
            elif thumb_type == ThumbType.DE_THUMB.value:
                if article:
                    _update_article_thumb(article, thumb=False)
                    serializer = self.serializer(data={"code": status.HTTP_200_OK, "msg": "取消点赞成功"})
                    return (
                        JsonResponse(serializer.data)
                        if serializer.is_valid()
                        else JsonResponse(serializer.errors, safe=False)
                    )
                else:
                    logger.error("failed with invalid article")
                    serializer = self.serializer(data={"code": status.HTTP_404_NOT_FOUND, "msg": "未找到文章"})
                    return (
                        JsonResponse(serializer.data)
                        if serializer.is_valid()
                        else JsonResponse(serializer.errors, safe=False)
                    )
            else:
                logger.error("failed with invalid params")
                serializer = self.serializer(data={"code": status.HTTP_400_BAD_REQUEST, "msg": "无效参数"})
                return (
                    JsonResponse(serializer.data)
                    if serializer.is_valid()
                    else JsonResponse(serializer.errors, safe=False)
                )
        except SecurityError as e:
            logger.error(f"failed with `{e}` while decrypt params")
            serializer = self.serializer(data={"code": status.HTTP_400_BAD_REQUEST, "msg": "解析ID失败"})
            return (
                JsonResponse(serializer.data) if serializer.is_valid() else JsonResponse(serializer.errors, safe=False)
            )
        except Exception as e:
            logger.error(f"failed with `{e}` while in (de)thumb article")
        serializer = self.serializer(data={"code": status.HTTP_400_BAD_REQUEST, "msg": "无效参数"})
        return JsonResponse(serializer.data) if serializer.is_valid() else JsonResponse(serializer.errors, safe=False)
