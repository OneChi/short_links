from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.generic import TemplateView

from .views import main_page, RedisTest

urlpatterns = [
    path('', main_page),
    path('test/', RedisTest.as_view(), name='test')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
