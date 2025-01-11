from django.urls import path

from . import views

urlpatterns = [
    # 页面路由
    path("login", views.login_page, name="login page"),
    path("logout", views.logout_page, name="logout page"),
    path("", views.user_detail_page, name="visitor detail page"),
    path("detail", views.user_detail_page, name="visitor detail page"),
    # API路由
    path("api/login", views.login, name="login api"),
    path("api/register", views.register, name="register api"),
    path("api/delete", views.cancel_user, name="cancel_user"),
    path("api/update", views.update_user, name="update_user"),
    path(
        "api/articles",
        views.get_specific_user_articles,
        name="get_specific_user_articles",
    ),
    path("api/software", views.get_specific_user_software, name="get_specific_user_software"),
    path("api/love/articles", views.get_specific_user_favorite_articles, name="get_specific_user_favorite_articles"),
    path(
        "api/love/software",
        views.get_specific_user_favorite_software,
        name="get_specific_user_questions",
    ),
]
