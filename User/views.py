
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Profile
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Q

# Create your views here.


# 主页面
def index(request):
    return JsonResponse("主页", safe=False)


# 用户登录
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            response = {'info': "Login Success!", 'userID': user.id, 'username': username}
            return JsonResponse(response)
        else:
            return JsonResponse("账号或密码输入有误。请重新输入!", safe=False)
    else:
        return JsonResponse("Invalid method", safe=False)


# 用户登出
def user_logout(request):
    logout(request)
    return JsonResponse("Logout Successfully!", safe=False)


# 用户注册
def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            return JsonResponse("两次密码不一致，请重新填写!", safe=False)
        else:
            try:
                exist = User.objects.get(Q(username=username))
                return JsonResponse("用户名已存在!", safe=False)
            except User.DoesNotExist:
                User.objects.create_user(username=username, password=password)
                response = {'info': "成功", 'usernameList': username}
                return JsonResponse(response)
    else:
        return JsonResponse("Invalid method", safe=False)


def get_usernamelist(request):
    if request.method == 'POST':
        ret = []
        users = User.objects.all()
        for user in users:
            ret.append(user.username)
        response = {'usernameList': ret}
        return JsonResponse(response)
    else:
        return JsonResponse("Invalid response", safe=False)


def profile(request, id):
    tmp = {}
    ret = []
    user = User.objects.get(id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
        print("get profile")
    else:
        profile = Profile.objects.create(user=user)
        print("create profile!")
    users = User.objects.all()
    namelist = []
    for x in users:
        namelist.append(x.username)
    tmp['usernameList'] = namelist
    tmp['id'] = user.id
    tmp['username'] = user.username
    tmp['age'] = profile.age
    tmp['hobby'] = profile.hobby
    tmp['introduction'] = profile.introduction
    tmp['gender'] = profile.gender
    tmp['email'] = user.email
    tmp['phone'] = profile.phone
    ret.append(tmp)

    return JsonResponse(ret, safe=False)


# @login_required(login_url='/User/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的字段
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    # asker_id = request.POST.get('id')
    # print(asker_id)
    # asker = User.objects.get(id=asker_id)

    if request.method == 'POST':
        # 验证用户是否是本人
        # if asker != user:
            # ret = []
            # ret.append(user)
            # retUser = serializers.serialize("json", ret)
            # response = {'user': retUser}
            # return JsonResponse(response)

        # profile_form = ProfileForm(request.POST, request.FILES)
        # if profile_form.is_valid():
            # 取得清洗后的合法数据
        # else:
            # uname = request.POST.get('username')  先不管username!
            phone = request.POST.get('phone')
            intro = request.POST.get('introduction')
            gender = request.POST.get('gender')
            hobby = request.POST.get('hobby')
            age = request.POST.get('age')
            email = request.POST.get('email')

            profile.phone = phone
            profile.introduction = intro
            profile.age = age
            profile.gender = gender
            profile.hobby = hobby
            # user.username = uname
            user.email = email
            # 如果图片存在FILES中
            # if 'img' in request.FILES:
                # profile.img = data["img"]
            profile.save()
            user.save()
            print(profile.introduction)
            print(user.email)
            return JsonResponse("成功", safe=False)


def change_password(request, id):
    user = User.objects.get(id=id)
    old_pwd = request.POST.get('formerPwd')
    new_pwd = request.POST.get('newPwd')
    if check_password(old_pwd, user.password):
        user.password = make_password(new_pwd)
        user.save()
        return JsonResponse("success", safe=False)
    else:
        return JsonResponse("failed", safe=False)
