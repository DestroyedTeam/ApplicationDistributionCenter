from django.urls import path
from . import views

urlpatterns = [
    path('search/result', views.search_result_page, name='search result page'),
    path('api/upload/image', views.upload_image, name='upload image api'),
    path('api/unload/image', views.unload_image, name='unload image api'),
]