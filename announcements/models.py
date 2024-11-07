from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Announcements(models.Model):
    """
    公告模型基本定义，形似sqlmodel或者sqlalchemy的模型定义
    不过在实际使用过程中比较简单，只需要继承models.Model即可
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='announcements', null=True, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    type = models.IntegerField(default=1, choices=((1, '全站'), (2, '指定APP')))
    app = models.ForeignKey('software.SoftWare', on_delete=models.CASCADE, null=True, blank=True)
    created_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs) -> None:
        # 如果没有指定 author，就使用当前登录的后台用户
        if not self.author:
            self.author = kwargs.pop('request').user
        super().save(*args, **kwargs)

    def short_title(self) -> str:
        """
        返回标题的前15个字符（短标题）
        """
        return self.title if len(self.title) <= 15 else f"{self.title[:15]}..."

    def short_content(self) -> str:
        """
        返回内容的前20个字符（短内容）
        """
        max_length = 20
        if len(self.content) > max_length:
            return f"{self.content[:max_length]}..."
        return self.content

    class Meta:
        ordering = ['-created_time']
        verbose_name = '公告管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
