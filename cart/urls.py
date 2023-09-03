from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.CartDetail.as_view(), name='details'),
    path('add/', views.CartAdd.as_view(), name='add'),
    path('remove/<int:pk>/', views.CartRemove.as_view(), name='remove'),
    path('show/', views.CartShow.as_view(), name='show'),
    path('add-single/', views.AddSingle.as_view(), name='add-single'),
    path('remove-single/', views.RemoveSingle.as_view(), name='remove-single'),
    path('compare/', views.CompareProduct.as_view(), name='compare'),
    path('compare/add/<int:pk>/', views.AddCompares.as_view(), name='add_compare'),
    path('compare/remove/', views.RemoveCompares.as_view(), name='compare_remove'),
]
