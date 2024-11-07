# Create your views here.

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django_router import router

from general.encrypt import decrypt
from general.init_cache import (get_all_category,
                                get_category_tags as g_c_ts)
from software.models import SoftWare


@require_GET
def category(request):
    if request.method == 'GET':
        categories = get_all_category()
        if len(categories) <= 0:
            return render(request, 'category.html',
                          {
                              'code': 406,
                              'error': 'Cache init failed, please contact the administrator.',
                          })
        try:
            category_id = request.GET.get('category_id')
            if category_id is None:
                return render(request, 'category.html',
                              {
                                  'code': 402,
                                  'error': 'wrong category_id',
                              })
            else:
                category_id = category_id.replace(' ', '+')
                category_id = int(decrypt(category_id))
        except ValueError:
            return render(request, 'category.html',
                          {
                              'code': 401,
                              'error': 'invalid category_id',
                          })
        except TypeError:
            return render(request, 'category.html',
                          {
                              'code': 400,
                              'error': 'wrong type of category_id',
                          })
        current_category_list = [cate for cate in categories if cate.id == category_id]
        if len(current_category_list) > 0:
            current_category = current_category_list[0]
            return render(request, 'category.html',
                          {
                              'category': current_category,
                              'software_set': current_category.software_set.all().filter(state=2)[:9],
                              'software_set_count': len(current_category.software_set.all().filter(state=2)),
                          })
        else:
            return render(request, 'category.html',
                          {
                              'code': 404,
                              'error': 'category not found',
                          })
    elif request.method == 'POST':
        categories = get_all_category()
        if len(categories) <= 0:
            return JsonResponse({
                'code': 406,
                'error': 'Cache init failed, please contact the administrator.',
            })
        try:
            category_id = request.POST.get('category_id')
            if category_id is None:
                return JsonResponse({
                    'code': 402,
                    'error': 'wrong category_id',
                })
            else:
                category_id = category_id.replace(' ', '+')
                category_id = int(decrypt(category_id))
        except ValueError:
            return JsonResponse({
                'code': 401,
                'error': 'invalid category_id',
            })
        except TypeError:
            return JsonResponse({
                'code': 400,
                'error': 'wrong type of category_id',
            })
        current_category_list = [cate for cate in categories if cate.id == category_id]
        if len(current_category_list) > 0:
            current_category = current_category_list[0]
            return JsonResponse({
                'code': 200,
                'data': {
                    'category':
                        {
                            'id': current_category.id,
                            'name': current_category.name,
                        },
                    'software_set':
                        [
                            {
                                'id': software.id,
                                'name': software.name,
                                'icon': software.icon.url,
                                'version': software.version,
                                'description': software.description,
                                'view_volume': software.view_volume,
                                'download_volume': software.download_volume,
                                'thumbs_volume': software.thumbs_volume,
                                'is_hot': software.is_hot(),
                                'is_recent': software.is_recent(),
                            } for software in current_category.software_set.all().filter(state=2)[9:]
                        ],
                    'software_set_count': len(current_category.software_set.all().filter(state=2)[9:]),
                }
            })
        else:
            return JsonResponse({
                'code': 404,
                'error': 'category not found',
            })
    else:
        return render(request, 'category.html', {
            'code': 405,
            'error': 'invalid request action',
        })


@require_POST
def get_category_tags(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        if category_id is None:
            return JsonResponse({'code': 402, 'error': 'wrong category_id'})
        else:
            try:
                category_id = int(decrypt(category_id))
                if category_id <= 0:
                    return JsonResponse({'code': 401, 'error': 'invalid category_id'})
                category_tags = [{'name': tag} for tag in g_c_ts(category_id)]
                return JsonResponse({
                    'code': 200,
                    'data': category_tags
                })
            except Exception as e:
                return JsonResponse({'code': 500, 'error': str(e)})
    else:
        return JsonResponse({'code': 405, 'error': 'invalid request action'})