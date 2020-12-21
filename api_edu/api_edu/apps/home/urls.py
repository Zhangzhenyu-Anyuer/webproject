from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve

from home import views

urlpatterns = [
    path('banner/',views.BannerListAPIView.as_view()),
    path('nav/',views.NavListAPIView.as_view()),
]