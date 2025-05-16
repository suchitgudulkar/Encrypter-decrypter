# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

# app_name = 'app'

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('', views.onboard, name='onboard'),
    path('dashboard', views.dashboard, name='home'),
    path('decrypt_file',views.decrypt_file, name='decrypt_file'),
    path('encrypt_file',views.encrypt_file, name='encrypt_file'),
]
