from django.urls import path

from .views import BackstageOverview, Rank

urlpatterns = [path("backstage-overview", BackstageOverview.as_view()), path("rank", Rank.as_view())]
