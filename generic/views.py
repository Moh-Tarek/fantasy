from django.shortcuts import render


def blank(request):
    return render(request, 'generic/base.html')