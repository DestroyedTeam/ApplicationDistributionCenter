from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework.decorators import APIView

from .serializers import AnalyticsSerializer, RankSerializer
from .utils import create_bar_chart, get_indicator, get_rank_data


class BackstageOverview(APIView):
    @staticmethod
    @login_required
    def get(request):
        try:
            serializer = AnalyticsSerializer(data={"indicators": get_indicator(), "chart": create_bar_chart()})
            if not serializer.is_valid():
                return render(request, "index.html", {"error": serializer.errors})
        except Exception as e:
            return render(request, "index.html", {"error": str(e)})
        return render(request, "index.html", serializer.data)


class RankView(APIView):
    @staticmethod
    @cache_page(60 * 15)
    def get(request):
        try:
            serializer = RankSerializer(data=get_rank_data())
            if not serializer.is_valid():
                return render(request, "rank.html", {"error": serializer.errors})
        except Exception as e:
            return render(request, "rank.html", {"error": str(e)})
        return render(request, "rank.html", serializer.data)
