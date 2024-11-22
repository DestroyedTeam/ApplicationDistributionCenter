# Create your views here.
import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from articles.models import Article
from general.encrypt import decrypt, encrypt
from general.init_cache import get_all_user, get_comments
from software.models import SoftWare

not_in_init_comments_parent = set()


@require_POST
def get_comments_data(request):
    comments = get_comments()
    if request.method == "POST":
        if comments:
            try:
                post_data = json.loads(request.body)
                query_id = decrypt(post_data["query_id"])
                query_type = post_data["type"]
            except ValueError:
                return JsonResponse({"code": 402, "msg": "failed with invalid params"})
            except TypeError:
                return JsonResponse({"code": 407, "msg": "failed with wrong params"})
            except AttributeError:
                return JsonResponse({"code": 401, "msg": "failed with bad request body"})
            if query_type == "article":
                comments = [
                    comment
                    for comment in comments
                    if comment.correlation_article and comment.correlation_article.id == int(query_id)
                ]
            if query_type == "software":
                comments = [
                    comment
                    for comment in comments
                    if comment.correlation_software and comment.correlation_software.id == int(query_id)
                ]
            if post_data.get("load_more"):
                comments = [t for t in comments if encrypt(str(t.id)).decode("utf8") not in not_in_init_comments_parent]
                if len(comments) < 10:
                    comments = None
                else:
                    comments = comments[10:]
            else:
                comments = comments[:10]
            if len(comments) <= 0:
                return JsonResponse({"code": 404, "msg": "failed with no data"})
            comments = [
                {
                    "comment_id": encrypt(str(comment.id)).decode("utf-8"),
                    "visitor": {
                        "user_id": encrypt(str(comment.visitor.id)).decode("utf-8"),
                        "username": comment.visitor.nickname if comment.visitor.nickname else comment.visitor.username,
                        "head_icon": comment.visitor.head_icon.url,
                        "role": comment.visitor.role,
                    },
                    "content": comment.content,
                    "correlation_article": comment.correlation_article.title if comment.correlation_article else "",
                    "correlation_software": comment.correlation_software.name if comment.correlation_software else "",
                    "created_time": comment.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "parent_id": encrypt(str(comment.parent.id)).decode("utf-8")
                    if comment.parent
                    else encrypt(str(0)).decode("utf-8"),
                }
                for comment in comments
            ]
            comments_id_list = [j["comment_id"] for j in comments]
            comments_id_list.append(encrypt(str(0)).decode("utf-8"))
            for i in comments:
                if i["parent_id"] not in comments_id_list:
                    not_in_init_comments_parent.add(i["parent_id"])
            for i in not_in_init_comments_parent:
                if query_type == "article":
                    t = [
                        t
                        for t in get_comments()
                        if i == encrypt(str(t.id)).decode("utf8") and t.correlation_article.id == int(query_id)
                    ][0]
                if query_type == "software":
                    t = [
                        t
                        for t in get_comments()
                        if i == encrypt(str(t.id)).decode("utf8") and t.correlation_software.id == int(query_id)
                    ][0]
                t = {
                    "comment_id": encrypt(str(t.id)).decode("utf-8"),
                    "visitor": {
                        "user_id": encrypt(str(t.user.id)).decode("utf-8"),
                        "username": t.visitor.nickname if t.visitor.nickname else t.visitor.username,
                        "head_icon": t.visitor.head_icon.url,
                        "role": t.visitor.role,
                    },
                    "content": t.content,
                    "correlation_article": t.correlation_article.title if t.correlation_article else "",
                    "correlation_software": t.correlation_software.name if t.correlation_software else "",
                    "created_time": t.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "parent_id": encrypt(str(t.parent.id)).decode("utf-8")
                    if t.parent
                    else encrypt(str(0)).decode("utf-8"),
                }
                comments.append(t)
            return JsonResponse({"code": 200, "msg": "success", "data": {"comments": comments}})
        else:
            return JsonResponse(
                {
                    "code": 404,
                    "msg": "failed with no data",
                }
            )
    else:
        return JsonResponse({"code": 301, "msg": "failed with wrong request action"})


@login_required
@require_POST
def publish_comment(request):
    if request.method == "POST":
        try:
            user = [mat_user for mat_user in get_all_user() if mat_user.username == request.user.username]
            if len(user) == 1:
                user = user[0]
            else:
                return JsonResponse({"code": 403, "msg": "请先登录"})
            content = request.POST.get("comment")
            correlation_article_id = int(decrypt(request.POST.get("article_id").encode("utf-8")))
            correlation_software_id = int(decrypt(request.POST.get("software_id").encode("utf-8")))
            parent_id = int(decrypt(request.POST.get("comment_parent").encode("utf-8")))
        except ValueError:
            return JsonResponse({"code": 402, "msg": "failed with invalid params"})
        except TypeError:
            return JsonResponse({"code": 401, "msg": "failed with wrong params"})
        except AttributeError:
            return JsonResponse({"code": 406, "msg": "failed with wrong request body"})
        if correlation_article_id:
            correlation_article = Article.objects.get(id=correlation_article_id)
        else:
            correlation_article = None
        if correlation_software_id:
            correlation_software = SoftWare.objects.get(id=correlation_software_id)
        else:
            correlation_software = None
        if parent_id:
            parent = user.comment_set.get(id=parent_id).filter(state=2)
        else:
            parent = None
        comment = user.comment_set.create(
            content=content,
            correlation_article=correlation_article,
            correlation_software=correlation_software,
            parent=parent,
        )
        if comment:
            return JsonResponse(
                {"code": 200, "msg": "success", "data": {"comment_id": encrypt(str(comment.id)).decode("utf-8")}}
            )
        else:
            return JsonResponse({"code": 400, "msg": "failed when inserting data to database"})
    else:
        return JsonResponse({"code": 301, "msg": "failed with invalid request action"})
