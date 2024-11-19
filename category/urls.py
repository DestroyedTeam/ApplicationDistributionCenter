from django.urls import path

from . import views

urlpatterns = [
    path("", views.category),
    path("api/tags", views.get_category_tags),
]
