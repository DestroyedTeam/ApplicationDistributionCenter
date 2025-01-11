from django.shortcuts import render


# Create your views here.
def custom_404_view(request, exception):
    # def custom_404_view(request):
    return render(
        request,
        "404.html",
        {
            "code": 404,
            "err": exception,
            # 'err': 'not found'
        },
    )


def custom_500_view(request):
    return render(request, "500.html", {"code": 500, "err": "服务器异常"})
