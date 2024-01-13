from django.db import models


# Create your models here.
class SoftWare(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()
    image = models.ImageField(upload_to='software')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = '软件管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
