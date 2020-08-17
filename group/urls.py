from django.urls import path
from . import views

app_name = 'group'

urlpatterns = [
    path('create_group/',views.create_group,name='create_group'),
    path('join_group/',views.join_group,name='join_group'),
    path('quit_group/',views.quit_group,name='quit_group'),
    path('set_admin/',views.set_admin,name='set_admin'),
    path('cancel_admin/',views.cancel_admin,name='cancel_admin'),
    path('test_post/',views.test_post,name='test_post'),
    path('get_users/',views.get_users,name='get_users'),
    path('get_groups/',views.get_groups,name='get_groups'),
    path('search_groups/',views.search_groups,name='search_groups'),
    path('test_doc/',views.test_doc,name='test_doc'),
    path('kick_out_user/',views.kick_out_user,name='kick_out_user'),
    path('dismiss_group/',views.dismiss_group,name='dismiss_group'),
    path('send_invitation/',views.send_invitation,name='send_invitation'),
    path('get_invitation_a/',views.get_invitation_a,name='get_invitation_a'),
    path('get_invitation_b/',views.get_invitation_b,name='get_invitation_b'),
    path('handle_invitation/',views.handle_invitation,name='handle_invitation'),
]