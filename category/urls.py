from django.urls import path

from .views import CategoryTagsView, CategoryView

urlpatterns = [
    path("api", CategoryView.as_view()),
    path("api/tags", CategoryTagsView.as_view()),
]
