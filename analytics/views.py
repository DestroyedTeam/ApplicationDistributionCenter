from datetime import datetime, timedelta
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from pyecharts import options as opts
from pyecharts.charts import Bar

from frontenduser.models import FrontEndUser
from general.common_compute import (get_article_hot_degree as g_h_a,
                                    get_software_hot_degree as g_h_s)
from general.init_cache import get_all_articles as g_a_as, get_all_software as g_a_s, get_all_user as g_a_u, \
    get_comments


# Create your views here.
def index(request):
    # 获取网站相关指标
    indicators = {}
    recent_appended_user = FrontEndUser.objects.filter(
        django_user__date_joined__gte=datetime.now() - timedelta(days=7)
    )
    indicators['recent_appended_user'] = {'name': '最近新增用户', 'value': len(recent_appended_user)}
    indicators['recent_appended_software'] = {'name': '最近新增软件', 'value': len(g_a_s())}
    indicators['all_user'] = {'name': '总用户数', 'value': len(g_a_u())}
    indicators['all_articles'] = {'name': '总文章数', 'value': len(g_a_as())}
    indicators['all_software'] = {'name': '总软件数', 'value': len(g_a_s())}
    indicators['all_views'] = {'name': '总浏览量',
                               'value': sum([i.view_volume for i in g_a_as()]) + sum([i.view_volume for i in g_a_s()])}
    indicators['all_downloads'] = {'name': '总下载量', 'value': sum([i.download_volume for i in g_a_s()])}
    indicators['all_comments'] = {'name': '总评论数',
                                  'value': len([comment for comment in get_comments()])}
    indicators['all_thumbs'] = {'name': '总点赞数',
                                'value': sum([i.thumbs_volume for i in g_a_as()]) + sum(
                                    [i.thumbs_volume for i in g_a_s()])}
    # 创建一个图表对象
    bar = Bar()
    sorted_software = sorted([s for s in g_a_s()], key=lambda x: g_h_s(x), reverse=True)
    x_list, y_list = [s.name for s in sorted_software][:10], [g_h_s(s) for s in sorted_software][:10]
    bar.add_xaxis(x_list)
    bar.add_yaxis("热度", y_list)
    sorted_software = sorted(sorted_software, key=lambda x: x.download_volume, reverse=True)
    x_list, y_list = [s.name for s in sorted_software][:10], [s.download_volume for s in sorted_software][:10]
    bar.add_xaxis(x_list)
    bar.add_yaxis("下载量", y_list)
    sorted_software = sorted(sorted_software, key=lambda x: x.view_volume, reverse=True)
    x_list, y_list = [s.name for s in sorted_software][:10], [s.view_volume for s in sorted_software][:10]
    bar.add_xaxis(x_list)
    bar.add_yaxis("点击量", y_list)
    sorted_software = sorted(sorted_software, key=lambda x: x.thumbs_volume, reverse=True)
    x_list, y_list = [s.name for s in sorted_software][:10], [s.thumbs_volume for s in sorted_software][:10]
    bar.add_xaxis(x_list)
    bar.add_yaxis("点赞", y_list)
    # 设置图表的全局配置项
    bar.set_global_opts(title_opts=opts.TitleOpts(title="软件概览"))
    return render(request, 'index.html',
                  {
                      'chart1': bar.dump_options_with_quotes(),
                      'indicators': indicators
                  })


@cache_page(30)
def rank(request):
    all_articles, all_software = g_a_as(), g_a_s()
    today_date = datetime.now().date()

    def get_top_items(items, key_func, top_n=10):
        sorted_items = sorted(items, key=key_func, reverse=True)[:top_n]
        if len(sorted_items) < top_n:
            sorted_items += [None] * (top_n - len(sorted_items))
        return sorted_items

    def filter_and_sort(items, date_field, date_value, key_func, top_n=10):
        filtered_items = [single_item for single_item in items if getattr(single_item, date_field).date() == date_value]
        return get_top_items(filtered_items, key_func, top_n)

    today_up_and_coming_star_articles = filter_and_sort(all_articles, 'updated_time', today_date, lambda x: x.updated_time)
    today_up_and_coming_star_software = filter_and_sort(all_software, 'updated_time', today_date, lambda x: x.updated_time)

    for item in all_articles:
        item.popularity = g_h_a(item, 2)
    for item in all_software:
        item.popularity = g_h_s(item, 2)

    today_popularity_articles = get_top_items([item for item in all_articles if item.popularity > 0], lambda x: x.popularity)
    today_popularity_software = get_top_items([item for item in all_software if item.popularity > 0], lambda x: x.popularity)

    all_time_up_and_coming_star_articles = get_top_items(all_articles, lambda x: x.updated_time)
    all_time_up_and_coming_star_software = get_top_items(all_software, lambda x: x.updated_time)

    for item in all_articles:
        item.popularity = g_h_a(item)
    for item in all_software:
        item.popularity = g_h_s(item)

    all_time_popularity_articles = get_top_items([item for item in all_articles if item.popularity > 0], lambda x: x.popularity)
    all_time_popularity_software = get_top_items([item for item in all_software if item.popularity > 0], lambda x: x.popularity)

    return render(request, 'rank.html', {
        'today_up_and_coming_star_articles': today_up_and_coming_star_articles,
        'today_up_and_coming_star_software': today_up_and_coming_star_software,
        'today_popularity_articles': today_popularity_articles,
        'today_popularity_software': today_popularity_software,
        'all_time_up_and_coming_star_articles': all_time_up_and_coming_star_articles,
        'all_time_up_and_coming_star_software': all_time_up_and_coming_star_software,
        'all_time_popularity_articles': all_time_popularity_articles,
        'all_time_popularity_software': all_time_popularity_software,
    })
