from django.urls import path
from . import views

app_name = 'doc'

urlpatterns = [
    path('save_doc/',views.save_doc,name='save_doc'),
    path('get_doc/',views.get_doc,name='get_doc'),
    path('submit_comment/',views.submit_comment,name='submit_comment'),
    path('get_comments/',views.get_comments,name='get_comments'),
    path('change_info/',views.change_info,name='change_info'),
    path('search_docs/',views.search_docs,name='search_docs'),
    path('match_edit/',views.match_edit,name='match_edit'),
    path('end_edit/',views.end_edit,name='end_edit'),
    path('get_groupnum/',views.get_groupnum,name='get_groupnum'),
]