from django.urls import path

from .views import NoticesView

urlpatterns = [path("api", NoticesView.as_view())]
