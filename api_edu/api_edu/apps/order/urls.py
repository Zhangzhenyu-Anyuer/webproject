from django.urls import path

from order import views

urlpatterns = [
    path('orderlist/', views.CartTotalPriceViewSet.as_view({'get': 'get_total_price'})),
    path('create/', views.OrderAPIView.as_view()),
]
