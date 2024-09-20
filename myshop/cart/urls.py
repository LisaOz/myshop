from django.urls import path
from . import views
app_name = 'cart'

"""
URL patterns for the views: add item to the cart, update quantity, remove item, display cart's contents
"""

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]