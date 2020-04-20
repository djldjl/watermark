from django.urls import path, include, re_path
from . import views

# app_name = 'watermarkapp'   # 不要这句也可以

urlpatterns = [
    path('', views.index, name='index'),
    path('file', views.filehandler, name='file'),
    path('download', views.download, name='download'),
    path('history', views.get_history, name='history'),
    path('limits', views.get_limits, name='limits'),
]
