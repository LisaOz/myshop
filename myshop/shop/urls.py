from django.urls import path
from . import views

"""
Define the URL patterns for the product cataloque.
"""

app_name = 'shop'
urlpatterns = [
    path('', views.product_list, name='product_list'), # url pattern for product_list view without parameters
    path(
        '<slug:category_slug>/',
        views.product_list,
        name='product_list_by_category' # filter products accoding by the category using slug parameter
    ),
    path(
        '<int:id>/<slug:slug>/',
        views.product_detail, # pattern to retrieve a specific product by the id and slug
        name='product_detail'
    ),
]