from django.urls import path

from .views import ArticleAPIView, ArticlePageView, ArticleThumbView

urlpatterns = [
    # 页面路由
    path("", ArticlePageView.as_view(), name="article(s) page"),
    # API路由
    # TODO: put[更新/修改文章,当前版本未实现], delete[删除文章,当前版本未实现]
    # 这个路由是一个标准的RESTful API，用于文章的各种操作(get[封装了单文章和文章列表获取], post[发表文章])
    path("api", ArticleAPIView.as_view(), name="get articles api"),
    path("api/thumb", ArticleThumbView.as_view(), name="thumb article api"),
]
