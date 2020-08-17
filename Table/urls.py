from django.urls import path
from . import views

app_name = 'Table'

urlpatterns = [
    path('', views.index, name='index'),
    path('recent/<int:id>/', views.recent_files, name='recent'),
    path('collect/<int:id>/', views.collect_files, name='collect'),
    path('myfiles/<int:id>/', views.my_files, name='myfiles'),
    path('bin/<int:id>/', views.bin_files, name='bin'),
    path('collect_file/', views.collect, name='collect_file'),
    path('delete_file/', views.delete_file, name='delete_file'),  # 个人空间内删除文档
    path('not_collect/', views.cancel_collect, name='not_collect'),  # 取消收藏文档
    path('recover_file/', views.recover_file, name='recover_file'),  # 恢复删除的文档
    path('delete_bin_file/', views.delete_bin_file, name='delete_file'),  # 删除回收站中某一个文件
    path('delete_bin_all/', views.delete_bin_all, name='delete_bin_all'),  # 删除回收站中所有文档
    path('new_file/', views.create_file, name='create_file'),  # 创建个人文档
 ]
