from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import CollectList, File
from django.core import serializers
from django.db.models import Q


# Create your views here.
def index(request):
    return JsonResponse("个人工作台", safe=False)


def recent_files(request, id):
    try:
        user = User.objects.get(id=id)
        # 获取user下的所有files
        files = user.files.all()  # files为related_name
        current_time = timezone.now()
        ret = []
        for file in files:
            print(current_time)
            print(file.lasttime)
            if (current_time - file.lasttime).days <= 3:
                ret.append(file)
        retfile = serializers.serialize("json", ret)
        response = {"files": retfile}

    except User.DoesNotExist:  # 没有这个用户 返回空值
        files = None
        response = {'files': files}
    return JsonResponse(response)


def collect_files(request, id):
    try:
        collectfiles = CollectList.objects.get(user_id=id)
        ret = []
        for file in collectfiles:
            ret.append(file)
    except CollectList.DoesNotExist:  # 没有收藏记录 返回空值
        ret = None
        response = {"files": ret}
        return JsonResponse(response)

    retfile = serializers.serialize("json", ret)
    response = {"files": retfile}
    return JsonResponse(response)


def my_files(request, id):
    try:
        user = User.objects.get(id=id)
        # 获取user下的所有files
        files = user.files.all()  # files为related_name
        ret = []
        for file in files:
            ret.append(file)
        retfile = serializers.serialize("json", ret)
        response = {"files": retfile}
    except User.DoesNotExist:  # 没有这个用户 返回空值
        files = None
        response = {'files': files}

    return JsonResponse(response)


def bin_files(request, id):
    try:
        user = User.objects.get(id=id)
        files = user.files.all()
        ret = []
        for file in files:
            if file.stat == -2:
                ret.append(file)
        retfile = serializers.serialize("json", ret)
        response = {"files": retfile}

    except User.DoesNotExist:  # 没有这个用户 返回空值
        files = None
        response = {'files': files}

    return JsonResponse(response)
