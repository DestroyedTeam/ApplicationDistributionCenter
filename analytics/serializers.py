from rest_framework import serializers


class IndicatorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    value = serializers.IntegerField(allow_null=True)


class AnalyticsSerializer(serializers.Serializer):
    class IndicatorsSerializer(serializers.Serializer):
        recent_appended_user = IndicatorSerializer(allow_null=True)
        recent_appended_software = IndicatorSerializer(allow_null=True)
        all_user = IndicatorSerializer(allow_null=True)
        all_articles = IndicatorSerializer(allow_null=True)
        all_software = IndicatorSerializer(allow_null=True)
        all_views = IndicatorSerializer(allow_null=True)
        all_downloads = IndicatorSerializer(allow_null=True)
        all_comments = IndicatorSerializer(allow_null=True)
        all_thumbs = IndicatorSerializer(allow_null=True)

    class ChartSerializer(serializers.Serializer):
        bar = serializers.CharField(allow_blank=True, allow_null=True)

    indicators = IndicatorsSerializer()
    chart = ChartSerializer()


class RankSerializer(serializers.Serializer):
    today_up_and_coming_star_articles = serializers.ListField()
    today_up_and_coming_star_software = serializers.ListField()
    today_popularity_articles = serializers.ListField()
    today_popularity_software = serializers.ListField()
    all_time_up_and_coming_star_articles = serializers.ListField()
    all_time_up_and_coming_star_software = serializers.ListField()
    all_time_popularity_articles = serializers.ListField()
    all_time_popularity_software = serializers.ListField()
