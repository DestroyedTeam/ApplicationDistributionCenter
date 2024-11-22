from loguru import logger

from general.encrypt import decrypt

from .models import Article


def filter_empty_string(*args) -> str | tuple | None:
    """
    过滤空字符串
    """
    filtered_args = tuple(arg for arg in args if arg and arg.strip() != "")
    if not filtered_args or len(filtered_args) <= 0:
        return None
    if len(filtered_args) == 1:
        return filtered_args[0]
    return filtered_args


class UpdateArticleViewVolume:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        # 调用原始视图方法
        response = self.func(*args, **kwargs)
        request = args[0]
        article_id = request.GET.get("article_id")

        if article_id:
            try:
                article_id = decrypt(article_id)
                article = Article.objects.get(id=article_id)
                article.view_volume += 1
                article.save()
            except (Article.DoesNotExist, ValueError, TypeError):
                logger.warning(f"未找到id为{article_id}的文章")

        return response
