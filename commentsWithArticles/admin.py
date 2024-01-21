from django.contrib import admin

from commentsWithArticles.models import Comment, Article


# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content', 'state', 'created_time', 'parent']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'content', 'state', 'created_time', 'updated_time']
