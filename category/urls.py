from django.urls import path

from .views import Category, CategoryTags

urlpatterns = [
    path("api", Category.as_view()),
    path("api/tags", CategoryTags.as_view()),
]
