from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from announcements.models import Announcements
from articles.models import Article
from category.models import Category
from comments.models import Comment
from favorites.models import Favorites
from questions.models import Questions
from software.models import SoftWare
from visitor.models import Visitor

from .common_compute import get_article_hot_degree, get_software_hot_degree


def _check_and_set_cache(key: str, value: QuerySet, timeout: int = 100):
    """
    检查缓存是否存在，如果不存在则设置缓存
    @param key: 缓存键
    @param value: 缓存值
    @param timeout: 缓存过期时间
    """
    actual_value = value if value.count() > 0 else []
    cache.set(key, actual_value, timeout)
    return actual_value


def get_notices(software_id: int = None) -> list[Announcements]:
    notices: list[Announcements] = cache.get("notices")
    if not notices:
        notices = list(Announcements.objects.filter().order_by("-created_time"))
        cache.set("notices", notices, 60 * 60)
    return cache.get("notices") if not software_id else [notice for notice in notices if notice.app.id == software_id]


def get_comments(
    software_id: int = None, article_id: int = None, page: int = None, page_size: int = None
) -> QuerySet[Comment]:
    # 如果没有传入 software_id 或 article_id，认为是无效请求
    if not software_id and not article_id:
        raise ValidationError("Either software_id or article_id must be provided to fetch comments.")

    # 根据传入参数构建缓存键
    if software_id:
        cache_key = f"comments:software:{software_id}:{page}"
    elif article_id:
        cache_key = f"comments:article:{article_id}:{page}"
    else:
        raise ValidationError("Either software_id or article_id must be provided to fetch comments.")

    # 尝试从缓存中获取数据
    comments = cache.get(cache_key)

    if comments is None:
        # 如果缓存中没有数据，查询数据库
        if software_id:
            comments = Comment.objects.filter(correlation_software_id=software_id)
        elif article_id:
            comments = Comment.objects.filter(correlation_article_id=article_id)

        # 尝试从缓存中获取数据
        comments = comments[(page - 1) * page_size : page * page_size]
        comments = _check_and_set_cache(cache_key, comments)

    elif comments.count() < page_size:
        comments = (
            Comment.objects.filter(correlation_software_id=software_id)
            if software_id
            else Comment.objects.filter(correlation_article_id=article_id)
        )
        comments = comments[(page - 1) * page_size : page * page_size]
        comments = _check_and_set_cache(cache_key, comments)
    return comments


def get_matched_articles_by_article_id(article_id=None):
    matched_articles = cache.get("article")
    if matched_articles is None:
        if article_id is None:
            cache.set("article", None, 15)
        else:
            matched_articles = list(Article.objects.filter(id=int(article_id), state=2).select_related("user"))
            cache.set("article", matched_articles, 15)
    elif article_id and len(matched_articles) > 0 and matched_articles[0].id != int(article_id):
        matched_articles = list(Article.objects.filter(id=int(article_id), state=2).select_related("user"))
        cache.set("article", matched_articles, 15)
    return cache.get("article")


def get_specific_user_articles_by_username(username=None):
    specific_user_articles = cache.get("specific_user_articles")
    if specific_user_articles is None:
        if username is None:
            cache.set("specific_user_articles", None, 30)
        else:
            specific_user_articles = list(
                Article.objects.filter(user__username=username, state=2)
                .select_related("user", "correlation_software")
                .order_by("-updated_time")
            )
            cache.set("specific_user_articles", specific_user_articles, 30)
    elif username and len(specific_user_articles) > 0 and specific_user_articles[0].visitor.username != username:
        specific_user_articles = list(
            Article.objects.filter(user__username=username, state=2)
            .select_related("user", "correlation_software")
            .order_by("-updated_time")
        )
        cache.set("specific_user_articles", specific_user_articles, 30)
    return cache.get("specific_user_articles")


def get_specific_user_favorite_articles_by_username(username=None):
    specific_user_articles = cache.get("specific_user_favorite_articles")
    if specific_user_articles is None:
        if username is None:
            cache.set("specific_user_favorite_articles", None, 15)
        else:
            specific_user_articles = list(
                Favorites.objects.filter(user__username=username, correlation_type=1)
                .select_related("visitor", "correlation_article")
                .filter(correlation_article__state=2)
                .order_by("-created_time")
            )
            cache.set("specific_user_favorite_articles", specific_user_articles, 15)
    elif username and len(specific_user_articles) > 0 and specific_user_articles[0].visitor.username != username:
        specific_user_articles = list(
            Favorites.objects.filter(user__username=username, correlation_type=1)
            .select_related("visitor", "correlation_article")
            .filter(correlation_article__state=2)
            .order_by("-created_time")
        )
        cache.set("specific_user_favorite_articles", specific_user_articles, 15)
    return cache.get("specific_user_favorite_articles")


def get_all_favorite_articles():
    favorite_articles = cache.get("favorite_articles")
    if favorite_articles is None:
        favorite_articles = list(
            Favorites.objects.filter(correlation_type=1, correlation_article__state=2)
            .select_related("visitor", "correlation_article")
            .order_by("-created_time")
        )
        cache.set("favorite_articles", favorite_articles, 45)
    return cache.get("favorite_articles")


def get_articles(article_id: int = None) -> QuerySet[Article]:
    all_articles: QuerySet[Article] = cache.get("all_articles")
    if article_id:
        filtered_single_article = all_articles.filter(id=article_id) if all_articles else None
        if filtered_single_article and len(filtered_single_article) > 0:
            return filtered_single_article
        return (
            Article.objects.all()
            .filter(id=article_id)
            .prefetch_related("user")
            .prefetch_related("correlation_software")
        )
    if not all_articles:
        all_articles = (
            Article.objects.filter(state=2)
            .prefetch_related("user")
            .prefetch_related("correlation_software")
            .order_by("-updated_time")
        )
        cache.set("all_articles", all_articles, 45)
    return cache.get("all_articles")


def get_software_by_software_id(software_id=None):
    software = cache.get("software")
    if software is None:
        if software_id is None:
            cache.set("software", None, 10)
        else:
            software = list(
                SoftWare.objects.filter(id=int(software_id), state=2)
                .select_related("user", "category")
                .prefetch_related("softwarescreenshots_set", "article_set")
            )
            cache.set("software", software, 10)
    elif software_id and len(software) > 0 and software[0].id != int(software_id):
        software = list(
            SoftWare.objects.filter(id=int(software_id), state=2)
            .select_related("user", "category")
            .prefetch_related("softwarescreenshots_set", "article_set")
        )
        cache.set("software", software, 10)
    return cache.get("software")


def get_software(software_id: int = None) -> QuerySet[SoftWare]:
    cache_key = f"software:{software_id}" if software_id else "all_software"
    software = cache.get(cache_key)
    if software is None:
        if software_id:
            software = SoftWare.objects.filter(id=software_id)
        else:
            software = (
                SoftWare.objects.filter(state=2)
                .order_by("-updated_time")
                .select_related("user", "category")
                .prefetch_related("softwarescreenshots_set")
            )
        software = _check_and_set_cache(cache_key, software)
    return software


def get_specific_user_software_by_username(username=None):
    specific_user_software = cache.get("specific_user_software")
    if specific_user_software is None:
        if username is None:
            cache.set("specific_user_software", None, 15)
        else:
            specific_user_software = list(
                SoftWare.objects.filter(user__username=username, state__lt=3)
                .select_related("user", "category")
                .prefetch_related("article_set")
                .order_by("-updated_time")
            )
            cache.set("specific_user_software", specific_user_software, 15)
    elif username and len(specific_user_software) > 0 and specific_user_software[0].visitor.username != username:
        specific_user_software = list(
            SoftWare.objects.filter(user__username=username, state=2)
            .select_related("user", "category")
            .prefetch_related("article_set")
            .order_by("-updated_time")
        )
        cache.set("specific_user_software", specific_user_software, 15)
    return cache.get("specific_user_software")


def get_all_user() -> QuerySet[Visitor]:
    all_user = cache.get("all_user")
    if all_user is None:
        all_user = Visitor.objects.filter(state=2).select_related("django_user").order_by("-django_user__date_joined")
        cache.set("all_user", all_user, 20)
    return cache.get("all_user")


def get_specific_user_favorite_software_by_username(username=None):
    """
    @param username: 用户名
    @return: 用户收藏的软件
    """
    specific_user_software = cache.get("specific_user_favorite_software")
    if specific_user_software is None:
        if username is None:
            cache.set("specific_user_software", None, 15)
        else:
            specific_user_software = list(
                Favorites.objects.filter(user__username=username, state=2)
                .select_related("visitor", "category", "correlation_software")
                .prefetch_related("article_set")
                .order_by("-updated_time")
            )
            cache.set("specific_user_favorite_software", specific_user_software, 15)
    elif username and len(specific_user_software) > 0 and specific_user_software[0].visitor.username != username:
        specific_user_software = list(
            Favorites.objects.filter(user__username=username, state=2)
            .select_related("visitor", "category", "correlation_software")
            .prefetch_related("article_set")
            .order_by("-updated_time")
        )
        cache.set("specific_user_favorite_software", specific_user_software, 15)
    return cache.get("specific_user_favorite_software")


def get_all_favorite_software():
    all_favorite_software = cache.get("favorite_software")
    if all_favorite_software is None:
        all_favorite_software = list(
            Favorites.objects.filter(correlation_type=2, correlation_software__state=2)
            .select_related("visitor", "correlation_software")
            .order_by("-created_time")
        )
        cache.set("favorite_software", all_favorite_software, 45)
    return cache.get("favorite_software")


def get_all_questions():
    all_questions = cache.get("all_questions")
    if all_questions is None:
        all_questions = list(Questions.objects.all().select_related("publisher").order_by("updated_time"))
        cache.set("all_questions", all_questions, 100)
    return cache.get("all_questions")


def get_all_answer():
    all_answer = cache.get("all_answer")
    if all_answer is None:
        all_answer = list(Questions.Answer.objects.all().select_related("respondent").order_by("created_time"))
        cache.set("all_answer", all_answer, 100)
    return cache.get("all_answer")


def get_all_category() -> QuerySet[Category]:
    categories = cache.get("categories")
    if categories is None:
        categories = Category.objects.filter(state=2).order_by("id").prefetch_related("software_set")
        cache.set("categories", categories, 60 * 10)
    return cache.get("categories")


def get_hot_articles_and_software():
    hot_articles = cache.get("hot_articles")
    hot_software = cache.get("hot_software")
    if hot_articles is None:
        hot_articles = list(Article.objects.filter(state=2))
        for article in hot_articles:
            article.hot_volume = get_article_hot_degree(article.id)
        hot_articles.sort(key=lambda x: x.hot_volume, reverse=True)
        cache.set("hot_articles", hot_articles[:10], 60 * 30)
    if hot_software is None:
        hot_software = list(SoftWare.objects.filter(state=2))
        for software in hot_software:
            software.hot_volume = get_software_hot_degree(software.id)
        hot_software.sort(key=lambda x: x.hot_volume, reverse=True)
        cache.set("hot_software", hot_software[:10], 60 * 30)
    return cache.get("hot_articles"), cache.get("hot_software")


def get_category_tags(category_id) -> list[str]:
    # 尝试从缓存中获取tags列表
    tags_cache_key = f"category_{category_id}_tags"
    unique_tags = cache.get(tags_cache_key)
    if unique_tags is None:
        # 如果缓存中没有找到，执行数据库查询并缓存结果
        unique_tags = list(SoftWare.objects.filter(category_id=category_id).values_list("tags", flat=True).distinct())
        cache.set(tags_cache_key, unique_tags, timeout=60 * 60)  # 缓存1小时
    else:
        # 如果缓存中找到了
        return unique_tags


@receiver(post_save, sender=Visitor)
@receiver(post_delete, sender=Visitor)
def refresh_cache_on_user_save(sender, instance, **kwargs):
    # 在Visitor保存后刷新相关缓存
    cache.delete("specific_user_articles")
    cache.delete("all_user")
    cache.delete("specific_user_software")


@receiver(post_delete, sender=Announcements)
@receiver(post_save, sender=Announcements)
def refresh_cache_on_notice_save(sender, instance, **kwargs):
    # 在Announcements保存后刷新相关缓存
    cache.delete("notices")


@receiver(post_delete, sender=Comment)
@receiver(post_save, sender=Comment)
def refresh_cache_on_comment_save(sender, instance, **kwargs):
    # 在Comment保存后刷新相关缓存
    cache.delete("comments")


@receiver(post_save, sender=Article)
@receiver(post_delete, sender=Article)
def refresh_cache_on_article_save(sender, instance, **kwargs):
    # 在Article保存后刷新相关缓存
    cache.delete("all_articles")
    cache.delete("specific_user_articles")
    cache.delete("hot_articles")


@receiver(post_save, sender=SoftWare)
@receiver(post_delete, sender=SoftWare)
def refresh_cache_on_software_save(sender, instance, **kwargs):
    # 在SoftWare保存后刷新相关缓存
    cache.delete("all_software")
    cache.delete("specific_user_software")
    cache.delete("hot_software")
    cache.delete(f"category_{instance.category_id}_tags")


@receiver(post_save, sender=Questions)
@receiver(post_delete, sender=Questions)
def refresh_cache_on_question_save(sender, instance, **kwargs):
    # 在Questions保存后刷新相关缓存
    cache.delete("all_questions")


@receiver(post_save, sender=Questions.Answer)
@receiver(post_delete, sender=Questions.Answer)
def refresh_cache_on_answer_save(sender, instance, **kwargs):
    # 在Questions.Answer保存后刷新相关缓存
    cache.delete("all_questions")
    cache.delete("all_answer")


@receiver(post_delete, sender=Category)
@receiver(post_save, sender=Category)
def refresh_cache_on_category_save(sender, instance, **kwargs):
    # 在Category保存后刷新相关缓存
    cache.delete("categories")
    cache.delete(f"category_{instance.id}_tags")
