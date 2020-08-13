from django.urls import path
from . import views

app_name = 'Table'

urlpatterns = [
    path('', views.index, name='index'),
    path('recent/<int:id>/', views.recent_files, name='recent'),
    path('collect/<int:id>/', views.collect_files, name='collect'),
    path('myfiles/<int:id>/', views.my_files, name='myfiles'),
    path('bin/<int:id>/', views.bin_files, name='bin'),
]
