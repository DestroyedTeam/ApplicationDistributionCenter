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
from typing import List, Any

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.views.static import serve
from django_router import router as rt
from analytics.views import index as ana, rank
from announcements.views import *
from testunit.views import *
from software.views import *
from category.views import *
from commentswitharticles.views import *
from questions.views import *
from frontenduser.views import *
from components.views import *
from error_handler.views import *

handler404 = custom_404_view
handler500 = custom_500_view

urlpatterns = [
                  # NOTE: these re_path are both valid in development and production environment.
                  re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
                  re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
                  re_path(r'^favicon.ico$', RedirectView.as_view(url=f'{settings.STATIC_ROOT}/favicon.ico')),
                  path('center/all/control/', admin.site.urls),
                  path('', home),
                  path('index/', home),
                  path('analytics/', ana),
                  path('articles/', articles_list),
                  path('article/details/', article_details),
                  path('rank/', rank),
                  path('search/', search_result),
                  path('questions/', init_questions),
                  path('software/details/', software_details),
                  path('login/', login),
                  path('logout/', logout),
                  path('user/details/', user_details),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + rt.urlpatterns
document_root = settings.STATIC_ROOT
# NOTE: The code is only valid in development environment. In production environment, the code will not work.

