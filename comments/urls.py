from django.urls import path

from .views import CommentView

urlpatterns = [
    path("api/all", CommentView.as_view(), name="get comments api"),
    # path("api/publish-comment", views.publish_comment, name="publish comment api"),
]
