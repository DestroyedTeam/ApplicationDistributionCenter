from django.db import models


# Create your models here.
class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=200)
    answer = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('frontenduser.FrontEndUser', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_time']
        verbose_name = '反馈中心'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.question
