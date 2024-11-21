from django.urls import path

from . import views

urlpatterns = [
    path("api/comments", views.get_comments_data, name="get comments api"),
    path("api/publish-comment", views.publish_comment, name="publish comment api"),
]
