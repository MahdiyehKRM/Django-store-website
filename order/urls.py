from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('information/', views.OrderInformation.as_view(), name='information'),
    path('coupon/<int:pk>/', views.CouponOrder.as_view(), name='coupon'),
    path('request/<int:pk>/', views.SendRequest.as_view(), name='request'),
    path('verify/', views.Verify.as_view(), name='verify'),
]
