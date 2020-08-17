from django.contrib import admin
from django.urls import path
from . import views

app_name = 'User'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('edit/<int:id>/', views.profile_edit, name='edit'),  # 提交修改的个人信息
    path('profile/<int:id>/', views.profile, name='profile'),
    path('register/usernameList/', views.get_usernamelist, name='usernameList'),
    path('change_password/<int:id>/', views.change_password, name='change_password'),  # 修改密码
]
