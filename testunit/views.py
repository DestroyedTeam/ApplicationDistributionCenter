from django.shortcuts import render


# Create your views here.
def test_modal(request):
    return render(request, "front/test_for_download_modal.html")
