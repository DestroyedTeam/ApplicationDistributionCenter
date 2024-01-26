from django.core.cache import cache

from announcements.models import Announcements
from commentsWithArticles.models import Comment, Article
from favorites.models import Favorites
from software.models import SoftWare


def get_notices():
    notices = cache.get('notices')
    if notices is None:
        notices = list(Announcements.objects.all().order_by('-date'))
        cache.set('notices', notices, 600)
    return cache.get('notices')


def get_comments():
    comments = cache.get('comments')
    if comments is None:
        comments = list(Comment.objects.filter(state=2)
                        .select_related('user', 'correlation_article', 'correlation_software')
                        .order_by('-created_time'))
        cache.set('comments', comments, 60)
    return cache.get('comments')


def get_matched_articles_by_article_id(article_id=None):
    matched_articles = cache.get('article')
    if matched_articles is None:
        if article_id is None:
            cache.set('article', None, 1)
        else:
            matched_articles = list(Article.objects.filter(id=int(article_id), state=2)
                           .select_related('user'))
            cache.set('article', matched_articles, 1)
    elif article_id and len(matched_articles) > 0 and matched_articles[0].id != int(article_id):
        matched_articles = list(Article.objects.filter(id=int(article_id), state=2)
                       .select_related('user'))
        cache.set('article', matched_articles, 1)
    return cache.get('article')


def get_specific_user_articles_by_username(username=None):
    specific_user_articles = cache.get('specific_user_articles')
    if specific_user_articles is None:
        if username is None:
            cache.set('specific_user_articles', None, 1)
        else:
            specific_user_articles = list(Article.objects.filter(user__username=username, state=2)
                                          .select_related('user', 'correlation_software')
                                          .order_by('-updated_time'))
            cache.set('specific_user_articles', specific_user_articles, 1)
    elif username and len(specific_user_articles) > 0 and specific_user_articles[0].user.username != username:
        specific_user_articles = list(Article.objects.filter(user__username=username, state=2)
                                      .select_related('user', 'correlation_software')
                                      .order_by('-updated_time'))
        cache.set('specific_user_articles', specific_user_articles, 1)
    return cache.get('specific_user_articles')


def get_specific_user_favorite_articles_by_username(username=None):
    specific_user_articles = cache.get('specific_user_articles')
    if specific_user_articles is None:
        if username is None:
            cache.set('specific_user_articles', None, 1)
        else:
            specific_user_articles = list(Favorites.objects.filter(user__username=username, correlation_type=1)
                                          .select_related('user', 'correlation_article').filter(correlation_article__state=2)
                                          .order_by('-created_time'))
            cache.set('specific_user_articles', specific_user_articles, 1)
    elif username and len(specific_user_articles) > 0 and specific_user_articles[0].user.username != username:
        specific_user_articles = list(Favorites.objects.filter(user__username=username, correlation_type=1)
                                      .select_related('user', 'correlation_article').filter(correlation_article__state=2)
                                      .order_by('-created_time'))
        cache.set('specific_user_articles', specific_user_articles, 1)
    return cache.get('specific_user_articles')


def get_all_favorite_articles():
    favorite_articles = cache.get('favorite_articles')
    if favorite_articles is None:
        favorite_articles = list(Favorites.objects.filter(correlation_type=1)
                        .select_related('user', 'correlation_article').filter(correlation_article__state=2)
                        .order_by('-created_time'))
        cache.set('favorite_articles', favorite_articles, 45)
    return cache.get('favorite_articles')


def get_all_articles():
    all_articles = cache.get('articles')
    if all_articles is None:
        all_articles = list(Article.objects.filter(state=2)
                        .select_related('user')
                        .order_by('-updated_time'))
        cache.set('articles', all_articles, 45)
    return cache.get('articles')


def get_software_by_software_id(software_id=None):
    software = cache.get('software')
    if software is None:
        if software_id is None:
            cache.set('software', None, 2)
        else:
            software = list(SoftWare.objects.filter(id=int(software_id), state=2)
                            .select_related('user', 'category')
                            .prefetch_related('softwarescreenshots_set'))
            cache.set('software', software, 2)
    elif software_id and len(software) > 0 and software[0].id != int(software_id):
        software = list(SoftWare.objects.filter(id=int(software_id), state=2)
                        .select_related('user', 'category')
                        .prefetch_related('softwarescreenshots_set'))
        cache.set('software', software, 2)
    return cache.get('software')


def get_all_software():
    all_software = cache.get('all_software')
    if all_software is None:
        all_software = list(SoftWare.objects.filter(state=2)
                         .select_related('user', 'category')
                         .prefetch_related('softwarescreenshots_set')
                         .order_by('-updated_time'))
        cache.set('all_software', all_software, 180)
    return cache.get('all_software')


def get_specific_user_software_by_username(username=None):
    specific_user_articles = cache.get('specific_user_articles')
    if specific_user_articles is None:
        if username is None:
            cache.set('specific_user_articles', None, 1)
        else:
            specific_user_articles = list(Article.objects.filter(user__username=username, state=2)
                                          .select_related('user', 'correlation_software')
                                          .order_by('-updated_time'))
            cache.set('specific_user_articles', specific_user_articles, 1)
    elif username and len(specific_user_articles) > 0 and specific_user_articles[0].user.username != username:
        specific_user_articles = list(Article.objects.filter(user__username=username, state=2)
                                      .select_related('user', 'correlation_software')
                                      .order_by('-updated_time'))
        cache.set('specific_user_articles', specific_user_articles, 1)
    return cache.get('specific_user_articles')


def get_specific_user_favorite_software_by_username(username=None):
    specific_user_articles = cache.get('specific_user_articles')
    if specific_user_articles is None:
        if username is None:
            cache.set('specific_user_articles', None, 1)
        else:
            specific_user_articles = list(Favorites.objects.filter(user__username=username, correlation_type=1)
                                          .select_related('user', 'correlation_article').filter(correlation_article__state=2)
                                          .order_by('-created_time'))
            cache.set('specific_user_articles', specific_user_articles, 1)
    elif username and len(specific_user_articles) > 0 and specific_user_articles[0].user.username != username:
        specific_user_articles = list(Favorites.objects.filter(user__username=username, correlation_type=1)
                                      .select_related('user', 'correlation_article').filter(correlation_article__state=2)
                                      .order_by('-created_time'))
        cache.set('specific_user_articles', specific_user_articles, 1)
    return cache.get('specific_user_articles')


def get_all_favorite_software():
    favorite_articles = cache.get('favorite_articles')
    if favorite_articles is None:
        favorite_articles = list(Favorites.objects.filter(correlation_type=1)
                        .select_related('user', 'correlation_article').filter(correlation_article__state=2)
                        .order_by('-created_time'))
        cache.set('favorite_articles', favorite_articles, 45)
    return cache.get('favorite_articles')