"""ApplicationDistributionCenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from components.views import home_page
from error_handler.views import custom_404_view, custom_500_view

handler404 = custom_404_view
handler500 = custom_500_view

urlpatterns = (
    [
        # NOTE: these re_path are both valid in development and production environment.
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
        re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
        # 后台路由
        path("center/all/control", admin.site.urls),
        # 前台路由
        path("", home_page),
        path("index/", home_page),
        path("analytics/", include("analytics.urls")),
        path("notices/", include("announcements.urls")),
        path("category/", include("category.urls")),
        path("articles/", include("articles.urls")),
        path("comments/", include("comments.urls")),
        path("common/", include("components.urls")),
        path("visitor/", include("visitor.urls")),
        path("software/", include("software.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(
        "/favicon.ico",
        document_root=f"{settings.STATIC_ROOT if settings.STATIC_ROOT else settings.STATICFILES_DIRS[0]}/favicon.ico",
    )
)
# NOTE: 加号后边的代码都是选择执行路由(即生产环境中可能不会执行)
