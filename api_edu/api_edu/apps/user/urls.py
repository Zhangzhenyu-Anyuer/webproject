from django.urls import path
from rest_framework_jwt.views import ObtainJSONWebToken

from user import views

urlpatterns = [
    path('login/',ObtainJSONWebToken.as_view()),
    path('captcha/',views.CaptchaAPIView.as_view()),
    path('register/',views.RegisterAPIView.as_view()),
    path('check/',views.CheckPhoneAPIView.as_view()),
    path('send/',views.SendMessageAPIView.as_view()),
]