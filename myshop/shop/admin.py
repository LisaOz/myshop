from django.contrib import admin
from .models import Category, Product


"""
Add models to the admin site to manage categories and products (add, delete, edit).
"""
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} # value is automatically set from other fields

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'price',
        'available',
        'created',
        'updated'
    ]
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available'] # fields can be edited from the display page of the admin site
    prepopulated_fields = {'slug': ('name',)}
# Register your models here.
