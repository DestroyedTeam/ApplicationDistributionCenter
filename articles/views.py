# Create your views here.
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.decorators import APIView

from general.common_compute import compute_similarity, get_related_articles
from general.common_exceptions import SecurityError
from general.data_handler import get_image_urls_from_md_str
from general.encrypt import decrypt
from general.init_cache import get_articles
from general.serializers import CommonResponseSerializer
from software.models import SoftWare

from .models import Article
from .serializers import ArticleSerializer


class ArticleAPIView(APIView):
    def __init__(self):
        super().__init__()
        self.serializer = CommonResponseSerializer

    def get(self, request):
        # id参数获取及校验
        article_id = request.GET.get("article_id")
        try:
            article_id = decrypt(article_id) if article_id else None
        except SecurityError:
            serializer = self.serializer(
                data={"code": status.HTTP_400_BAD_REQUEST, "msg": "failed with decrypt params"}
            )
            if serializer.is_valid():
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, safe=False)
        except Exception:
            serializer = self.serializer(
                data={"code": status.HTTP_400_BAD_REQUEST, "msg": "failed with invalid params"}
            )
            if serializer.is_valid():
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, safe=False)
        articles = get_articles() if not article_id else get_articles(article_id=article_id)

        # 页面参数获取及校验
        try:
            if (not article_id) and request.GET.get("page"):
                page_num = int(request.GET.get("page"))
            else:
                page_num = -1
        except Exception:
            serializer = self.serializer(
                data={"code": status.HTTP_400_BAD_REQUEST, "msg": "failed with invalid params"}
            )
            if serializer.is_valid():
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, safe=False)
        if page_num and page_num > 0:
            page_num -= 1
            articles = articles.filter()[page_num * 6 : page_num * 6 + 6]

        if articles and len(articles) > 0:
            article_serializer = ArticleSerializer(articles, many=True)
            if article_serializer.data:
                articles = [
                    {
                        "id": article.id,
                        "visitor": {
                            "user_id": article.user.id,
                            "username": article.user.username,
                            "email": article.user.django_user.email,
                        },
                        "title": article.title,
                        "content": article.content,
                        "correlation_software": article.correlation_software,
                        "created_time": article.created_time,
                        "updated_time": article.updated_time,
                    }
                    for article in articles
                ]
            else:
                serializer = self.serializer(
                    data={"code": status.HTTP_400_BAD_REQUEST, "msg": "failed with invalid data"}
                )
                if serializer.is_valid():
                    return JsonResponse(serializer.data)
                return JsonResponse(serializer.errors, safe=False)
            serializer = self.serializer(data={"code": status.HTTP_200_OK, "msg": "success", "data": articles})
            if serializer.is_valid():
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, safe=False)
        else:
            serializer = self.serializer(data={"code": status.HTTP_204_NO_CONTENT, "msg": "获取成功但空数据"})
            if serializer.is_valid():
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, safe=False)

    def post(self, request):
        try:
            title = request.POST.get("title")
            content = request.POST.get("content")
            cover = get_image_urls_from_md_str(content)
            if cover is None or len(cover) <= 0:
                cover = None
            else:
                cover = [c for c in cover if c.split(".")[-1] in ["jpg", "jpeg", "png", "gif"]]
                if len(cover) > 0:
                    cover = cover[0].replace("/media/", "")
                else:
                    cover = None
            correlation_software_id = request.POST.get("correlation_software_id")
            if correlation_software_id:
                correlation_software = SoftWare.objects.get(id=correlation_software_id)
            else:
                correlation_software = None
            if cover:
                article = Article.objects.create(
                    user=None, title=title, content=content, cover=cover, correlation_software=correlation_software
                )
            else:
                article = Article.objects.create(
                    user=None, title=title, content=content, correlation_software=correlation_software
                )
            if article:
                return JsonResponse({"code": 200, "msg": "success", "data": {"article_id": article.id}})
            else:
                return JsonResponse({"code": 400, "msg": "failed when inserting data to database"})
        except Exception:
            pass

    def put(self, request):
        pass

    def delete(self, request):
        pass


class ArticlePageView(APIView):
    def __init__(self):
        super().__init__()
        self.serializer = ArticleSerializer

    def get(self, request):
        article_id = request.GET.get("article_id")
        try:
            article_id = decrypt(article_id.replace(" ", "+")) if article_id else None
        except SecurityError:
            return render(request, "article_details.html", {"error": "解析ID失败", "code": status.HTTP_400_BAD_REQUEST})
        except Exception:
            return render(request, "article_details.html", {"error": "无效参数", "code": status.HTTP_400_BAD_REQUEST})
        articles = get_articles().filter()[:6] if not article_id else get_articles(article_id=article_id).filter()
        serializer = self.serializer(articles, many=True)
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


@require_POST
def thumb_article(request):
    if request.method == "POST":
        try:
            post_data = json.loads(request.body)
            thumb_type = post_data["thumb_type"]
            article_id = post_data["article_id"]
            article_id = str(article_id.replace(" ", "+"))
            article_id = decrypt(article_id)
            article = Article.objects.get(id=article_id)
            if thumb_type == "thumb":
                if article:
                    article.thumbs_volume += 1
                    article.save()
                    return JsonResponse({"code": 200})
                else:
                    return JsonResponse({"code": 404, "error": "Error with not found article"})
            elif thumb_type == "de_thumb":
                if article:
                    article.thumbs_volume -= 1
                    article.save()
                    return JsonResponse({"code": 200})
                else:
                    return JsonResponse({"code": 404, "error": "Error with not found article"})
        except ValueError:
            return JsonResponse({"code": 401, "error": "Error with invalid params"})
        except TypeError:
            return JsonResponse({"code": 402, "error": "Error with wrong params"})
        except AttributeError:
            return JsonResponse({"code": 400, "error": "Error with bad params"})
        else:
            return JsonResponse({"code": 406, "error": "Error with bad request headers"})
    else:
        return JsonResponse({"code": 405, "error": "Error with bad request action"})


@require_POST
def viewed_article(request):
    if request.method == "POST":
        try:
            article_id = request.POST.get("article_id")
            article_id = str(article_id.replace(" ", "+"))
            article_id = decrypt(article_id)
            article = Article.objects.get(id=article_id)
            if article:
                article.view_volume += 1
                article.save()
                return JsonResponse({"code": 200})
            else:
                return JsonResponse({"code": 404, "error": "Error with not found article"})
        except ValueError:
            return JsonResponse({"code": 401, "error": "Error with invalid params"})
        except TypeError:
            return JsonResponse({"code": 402, "error": "Error with wrong params"})
        except AttributeError:
            return JsonResponse({"code": 400, "error": "Error with bad params"})
    else:
        return JsonResponse({"code": 405, "error": "Error with bad request action"})
