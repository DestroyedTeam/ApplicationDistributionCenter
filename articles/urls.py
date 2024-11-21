from django.urls import path

from . import views

urlpatterns = [
    # 页面路由
    path("article", views.article_page, name="single article page"),
    path("articles", views.articles_page, name="articles list page"),
    path("publish", views.publish_page, name="publish page"),
    # API路由
    path("api/articles", views.get_articles, name="get articles api"),
    path("api/publish-article", views.publish_article, name="publish article api"),
    path("api/article/thumb", views.thumb_article, name="thumb article api"),
    path("api/article/viewed", views.viewed_article, name="viewed article api"),
    path("api/comments", views.get_comments_data, name="get comments api"),
    path("api/publish-comment", views.publish_comment, name="publish comment api"),
]
