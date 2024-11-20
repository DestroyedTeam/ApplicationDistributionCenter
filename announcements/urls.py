from django.urls import path

from .views import Notices

urlpatterns = [path("api", Notices.as_view())]
