from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('test/', views.test, name='test'),
    path('change_stat/', views.change_stat, name='change_stat'),
    path('set_user_auth/', views.set_user_auth, name='set_user_auth'),
    path('set_doc_auth/', views.set_doc_auth, name='set_doc_auth'),
    path('match_auth/', views.match_auth, name='match_auth'),
    path('set_group_auth/',views.set_group_auth,name='set_group_auth'),
    path('set_admin_auth/',views.set_admin_auth,name='set_admin_auth'),
]
