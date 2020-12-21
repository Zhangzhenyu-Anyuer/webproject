from rest_framework.generics import ListAPIView

from home.models import Banner, Nav
from home.serializers import BannerModelSerializer, NavModelSerializer


class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_delete=False,is_show=True).order_by('orders')
    serializer_class = BannerModelSerializer


class NavListAPIView(ListAPIView):
    queryset = Nav.objects.filter(is_delete=False,is_show=True)
    serializer_class = NavModelSerializer