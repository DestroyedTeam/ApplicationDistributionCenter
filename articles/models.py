import bs4
import markdown
from django.db import models


# Create your models here.
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("visitor.Visitor", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    cover = models.ImageField(upload_to="article", default="article/default.png")
    correlation_software = models.ForeignKey("software.SoftWare", on_delete=models.CASCADE, null=True, blank=True)
    state = models.IntegerField(default=1, choices=((1, "待审核"), (2, "正常"), (3, "拒绝")))
    view_volume = models.BigIntegerField(default=0)
    thumbs_volume = models.BigIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def short_title(self) -> str:
        max_length = 15
        if len(self.title) > max_length:
            return f"{self.title[:max_length]}..."
        return self.title

    def html_content(self) -> str:
        """
        从已存储的md文档转换获取HTML内容
        """
        md_content = markdown.markdown(self.content)
        return md_content

    def plain_content(self) -> str:
        """
        获取纯文本内容
        """
        html_content = markdown.markdown(self.content)
        soup = bs4.BeautifulSoup(html_content, "html.parser")
        return soup.get_text()

    def short_content(self) -> str:
        max_length = 20
        if len(self.plain_content()) > max_length:
            return f"{self.plain_content()[:max_length]}..."
        return self.plain_content()

    class Meta:
        ordering = ["-updated_time"]
        verbose_name = "文章管理"
        verbose_name_plural = verbose_name
        unique_together = ("title", "correlation_software")

    def __str__(self):
        return self.title
