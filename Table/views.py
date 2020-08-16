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


def recent_files(request, id):  # 返回收藏的状态
    try:
        user = User.objects.get(id=id)
        File.objects.create(doctitle="测试文档2", docintro="又要写后端了", doctext="啊啊啊小学期!", docname="开发日志3",
                            author=user, lastauthor=user)
        # 获取user下的所有files
        files = user.files.all()  # files为related_name
        current_time = timezone.now()
        ret = []
        for file in files:  # 加上收藏情况
            tmp = {}
            if (current_time - file.lasttime).days <= 3 and file.stat > -2:
                tmp['docnum'] = file.id
                tmp['docname'] = file.docname
                tmp['doctitle'] = file.doctitle
                tmp['docintro'] = file.docintro
                tmp['author'] = file.author_id
                tmp['lasttime'] = file.lasttime
                ret.append(tmp)

    except User.DoesNotExist:  # 没有这个用户 返回空值
        ret = []

    return JsonResponse(ret, safe=False)


def collect_files(request, id):
    try:
        user = User.objects.get(id=id)
        collectfiles = CollectList.objects.filter(user=user)
        ret = []
        for record in collectfiles:
            file = File.objects.get(id=record.file_id)  # 取得相应的文章
            tmp = {}
            tmp['docname'] = file.docname
            tmp['doctitle'] = file.doctitle
            tmp['docintro'] = file.docintro
            tmp['author'] = file.author_id
            tmp['lasttime'] = file.lasttime
            ret.append(tmp)
    except CollectList.DoesNotExist:  # 没有收藏记录 返回空值
        ret = []

    return JsonResponse(ret, safe=False)


def my_files(request, id):  # 返回收藏的状态
    try:
        ret = []
        user = User.objects.get(id=id)
        # 获取user下的所有files
        files = user.files.all()  # files为related_name
        for file in files:  # # 加上收藏情况
            if file.stat > -2:   # 不是被删除的
                tmp = {}
                tmp['docnum'] = file.id
                tmp['docname'] = file.docname
                tmp['doctitle'] = file.doctitle
                tmp['docintro'] = file.docintro
                tmp['author'] = file.author_id
                tmp['lasttime'] = file.lasttime
                ret.append(tmp)
    except User.DoesNotExist:  # 没有这个用户 返回空值
        ret = []

    return JsonResponse(ret, safe=False)


def bin_files(request, id):
    try:
        user = User.objects.get(id=id)
        files = user.files.all()
        ret = []
        for file in files:
            tmp = {}
            current = timezone.now()
            if file.stat == -2:
                if (current - file.deletetime).days > 7:  # 超过七天数据库删除
                    file.delete()
                    continue
                tmp['docnum'] = file.id
                tmp['docname'] = file.docname
                tmp['doctitle'] = file.doctitle
                tmp['docintro'] = file.docintro
                tmp['author'] = file.author_id
                tmp['lasttime'] = file.lasttime
                ret.append(tmp)

    except User.DoesNotExist:  # 没有这个用户 返回空值
        ret = []

    return JsonResponse(ret, safe=False)


def collect(request):
    id = request.POST.get('id')
    file_id = request.POST.get('file_id')
    print(id)
    print(file_id)
    user = User.objects.get(id=id)
    try:
        file = File.objects.get(id=file_id)
        if CollectList.objects.filter(user=user, file=file).exists():
            return JsonResponse("success", safe=False)  # 收藏文档成功
        else:
            CollectList.objects.create(user=user, file=file)
    except File.DoesNotExist:
        return JsonResponse("failed", safe=False)  # 文档不存在

    return JsonResponse("success", safe=False)  # 收藏文档成功


def delete_file(request):
    file_id = request.POST.get('file_id')
    try:
        file = File.objects.get(id=file_id)
        print(file)
        file.stat = -2
        file.deletetime = timezone.now()
        file.save()
    except File.DoesNotExist:  # 要删除的文档不存在
        return JsonResponse("failed", safe=False)
    return JsonResponse("success", safe=False)


def cancel_collect(request):  # 取消收藏
    return JsonResponse("success", safe=False)


def recover_file(request):
    file_id = request.POST.get('file_id')
    try:
        file = File.objects.get(id=file_id)
        file.stat = 0
        file.deletetime = None  # 重新恢复了
        file.save()
    except File.DoesNotExist:  # 要恢复的文档不存在
        return JsonResponse("failed", safe=False)
    return JsonResponse("success", safe=False)


def delete_bin_file(request):
    file_id = request.POST.get('file_id')
    try:
        file = File.objects.get(id=file_id)
        file.delete()
    except File.DoesNotExist:  # 要删除的文档不存在
        return JsonResponse("failed", safe=False)
    return JsonResponse("success", safe=False)


def delete_bin_all(request):
    file_array = request.POST.get('array')
    for file in file_array:
        try:
            delete_file = File.objects.get(id=file.id)
            delete_file.delete()
        except File.DoesNotExist:
            return JsonResponse("failed", safe=False)
    return JsonResponse("success", safe=False)




