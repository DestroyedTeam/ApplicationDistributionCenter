from django.urls import path

from . import views

urlpatterns = [path("backstage-overview", views.index), path("rank", views.rank)]
