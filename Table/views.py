from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q


# Create your views here.
def index(request):
    return JsonResponse("个人工作台", safe=False)


def recent_files(request, id):
    user = User.objects.get(id=id)
    # 获取user下的所有files
    files = user.files.all()  # files为related_name
    current_time = timezone.now()
    ret = []
    for file in files:
        if (current_time - file.lasttime).days <= 3:
            ret.append(file)
    response = {"files": ret}
    return JsonResponse(response)


def collect_files(request, id):
    return JsonResponse()


def my_files(request, id):
    user = User.objects.get(id=id)
    # 获取user下的所有files
    files = user.files.all()  # files为related_name
    ret = []
    for file in files:
        ret.append(file)
    response = {"files": ret}
    return JsonResponse(response)


def bin_files(request, id):
    user = User.objects.get(id=id)
    files = user.files.all()
    ret = []
    for file in files:
        if file.stat == -2:
            ret.append(file)
    response = {"files": ret}
    return JsonResponse(response)