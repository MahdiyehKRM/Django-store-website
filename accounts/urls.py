from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/<int:pk>/', views.ProfileUser.as_view(), name='profile'),
    path('update/<int:pk>/', views.UpdateUser.as_view(), name='update'),
    path('change/<int:pk>/', views.ChangeUser.as_view(), name='change'),
    path('phone/', views.PhoneForgot.as_view(), name='phone'),
    path('verify/', views.VerifyForgot.as_view(), name='verify'),
    path('confirm/<int:pk>/', views.ConfirmForgot.as_view(), name='confirm'),
    path('phone_login/', views.LoginPhone.as_view(), name='phone_login'),
    path('phone_verify/', views.VerifyPhone.as_view(), name='phone_verify'),


]
