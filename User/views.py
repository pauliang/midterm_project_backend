from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
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
            return JsonResponse("Login Success!", safe=False)
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
                return JsonResponse("成功", safe=False)
    else:
        return JsonResponse("Invalid method", safe=False)


@login_required(login_url='/User/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的字段
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        # 验证用户是否是本人
        if request.user != user:
            return HttpResponse("权限不足!")

        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            data = profile_form.cleaned_data
            profile.phone = data['phone']
            profile.introduction = data['introduction']
            # 如果图片存在FILES中
            if 'img' in request.FILES:
                profile.img = data["img"]

            profile.save()
            return render(request, 'index.html', locals())
        else:
            return HttpResponse("修改表单有误，请重新输入!")
    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, 'profile': profile, 'user': user}
        return render(request, 'edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")