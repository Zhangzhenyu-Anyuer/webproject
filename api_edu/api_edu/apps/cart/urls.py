from django.urls import path

from cart import views

urlpatterns = [
    path('option/', views.CartViewSet.as_view(
        {'post': 'add_cart', 'get': 'show_list', 'delete': 'del_course'})),
    path('cart_len/', views.CartLengthAPIView.as_view()),
    path('selected/', views.CartSelectedViewSet.as_view({'post': 'change_selected'})),
    path('expire/', views.CartExpireChangeViewSet.as_view({'post': 'change_expire'})),
    path('total/', views.TotalPriceViewSet.as_view({'get': 'update_total_price'})),
]
