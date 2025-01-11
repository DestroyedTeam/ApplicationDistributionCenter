from django.urls import path

from .views import BackstageOverview, RankView

urlpatterns = [path("backstage-overview", BackstageOverview.as_view()), path("rank", RankView.as_view())]
