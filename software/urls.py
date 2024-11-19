from django.urls import path

from . import views

urlpatterns = [
    # 页面路由
    path("", views.software_detail_page, name="software_page"),
    # API路由
    path("api/software", views.get_software, name="get_software api"),
    path("api/detail", views.get_software_detail, name="get_software_detail api"),
    path("api/publish", views.publish_software, name="publish_software api"),
    path("api/update/metric", views.update_software_metrics, name="update software metrics api"),
]
