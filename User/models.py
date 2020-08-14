from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# 用户的扩展信息
class Profile(models.Model):
    # 与自带的User模型形成一一对应的关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    # 头像
    img = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    # 简介
    introduction = models.TextField(max_length=200, blank=True, null=True)
    # 兴趣爱好
    hobby = models.TextField(max_length=100, blank=True, null=True)
    # 年龄
    age = models.IntegerField(blank=True, default=0, null=True)
    # 性别
    gender = models.IntegerField(blank=True, default=0, null=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)


