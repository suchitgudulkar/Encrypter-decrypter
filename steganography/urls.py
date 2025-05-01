from django.urls import path
from . import views

app_name = 'steganography'

urlpatterns = [
    path('', views.steganography_info, name='info'),
    path('encode/', views.encode, name='encode'),
    path('decode/', views.decode, name='decode'),
    path('download/<str:filename>/', views.download_file, name='download_file'),
]