from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('products/', views.AllProduct.as_view(), name='products'),
    path('category/<int:pk>/<slug:slug>/', views.AllProduct.as_view(), name='category'),
    path('details/<int:pk>/', views.ProductDetails.as_view(), name='details'),
    path('comment/<int:pk>/', views.CommentProduct.as_view(), name='comment'),
    path('reply/<int:pk>/<int:comment_id>/', views.ReplyCreateView.as_view(), name='product_reply'),
    path('favourite/<int:pk>/', views.FavouriteCreateView.as_view(), name='favourite_list'),

]
