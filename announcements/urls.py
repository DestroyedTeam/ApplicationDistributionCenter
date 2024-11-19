from django.urls import path

from . import views

urlpatterns = [path("api/all", views.get_notice_to_all), path("api/one", views.get_specific_app_notice)]
