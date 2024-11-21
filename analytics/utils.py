from datetime import datetime, timedelta, timezone

from pyecharts import options as opts
from pyecharts.charts import Bar

from general.common_compute import get_article_hot_degree, get_software_hot_degree
from general.init_cache import get_all_software, get_all_user, get_articles, get_comments


def get_indicator():
    all_user, all_articles, all_software = get_all_user(), get_articles(), get_all_software()
    recent_appended_user = [
        user for user in all_user if user.django_user.date_joined >= datetime.now(tz=timezone.utc) - timedelta(days=7)
    ]
    recent_appended_software = [
        software for software in all_software if software.created_time >= datetime.now() - timedelta(days=7)
    ]
    return {
        "recent_appended_user": {"name": "最近新增用户", "value": len(recent_appended_user)},
        "recent_appended_software": {"name": "最近新增软件", "value": len(recent_appended_software)},
        "all_user": {"name": "总用户数", "value": len(all_user)},
        "all_articles": {"name": "总文章数", "value": len(all_articles)},
        "all_software": {"name": "总软件数", "value": len(all_software)},
        "all_views": {
            "name": "总浏览量",
            "value": sum(i.view_volume for i in all_articles) + sum(i.view_volume for i in all_software),
        },
        "all_downloads": {"name": "总下载量", "value": sum(i.download_volume for i in all_software)},
        "all_comments": {"name": "总评论数", "value": len(get_comments())},
        "all_thumbs": {
            "name": "总点赞数",
            "value": sum(i.thumbs_volume for i in all_articles) + sum(i.thumbs_volume for i in all_software),
        },
    }


def create_bar_chart():
    bar = Bar()
    sorted_software = sorted(get_all_software(), key=lambda x: get_software_hot_degree(x), reverse=True)
    for metric, label in [
        ("热度", get_software_hot_degree),
        ("下载量", lambda x: x.download_volume),
        ("点击量", lambda x: x.view_volume),
        ("点赞", lambda x: x.thumbs_volume),
    ]:
        x_list, y_list = [s.name for s in sorted_software][:10], [label(s) for s in sorted_software][:10]
        bar.add_xaxis(x_list)
        bar.add_yaxis(metric, y_list)
        sorted_software = sorted(sorted_software, key=label, reverse=True)
    bar.set_global_opts(title_opts=opts.TitleOpts(title="软件概览"))
    return {"bar": bar.dump_options_with_quotes()}


def get_rank_data():
    def get_top_items(items, key_func, top_n=10):
        sorted_items = sorted(items, key=key_func, reverse=True)[:top_n]
        return sorted_items + [None] * (top_n - len(sorted_items))

    def filter_and_sort(items, date_field, date_value, key_func, top_n=10):
        filtered_items = [item for item in items if getattr(item, date_field).date() == date_value]
        return get_top_items(filtered_items, key_func, top_n)

    all_articles, all_software = get_articles(), get_all_software()
    today_date = datetime.now().date()

    update_popularity = lambda items, popularity_func, factor=1: [
        setattr(item, "popularity", popularity_func(item, factor)) for item in items
    ]

    update_popularity(all_articles, get_article_hot_degree, 2)
    update_popularity(all_software, get_software_hot_degree, 2)

    return {
        "today_up_and_coming_star_articles": filter_and_sort(
            all_articles, "updated_time", today_date, lambda x: x.updated_time
        ),
        "today_up_and_coming_star_software": filter_and_sort(
            all_software, "updated_time", today_date, lambda x: x.updated_time
        ),
        "today_popularity_articles": get_top_items(
            [item for item in all_articles if item.popularity > 0], lambda x: x.popularity
        ),
        "today_popularity_software": get_top_items(
            [item for item in all_software if item.popularity > 0], lambda x: x.popularity
        ),
        "all_time_up_and_coming_star_articles": get_top_items(all_articles, lambda x: x.updated_time),
        "all_time_up_and_coming_star_software": get_top_items(all_software, lambda x: x.updated_time),
        "all_time_popularity_articles": get_top_items(
            [item for item in all_articles if item.popularity > 0], lambda x: x.popularity
        ),
        "all_time_popularity_software": get_top_items(
            [item for item in all_software if item.popularity > 0], lambda x: x.popularity
        ),
    }
