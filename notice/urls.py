from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    path('get_notice/',views.get_notice,name='get_notice'),
]