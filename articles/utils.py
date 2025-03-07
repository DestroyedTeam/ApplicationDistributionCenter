from general.encrypt import decrypt
from utils.logger import logger

from .models import Article


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
