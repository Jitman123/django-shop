from django.contrib import admin

# Register your models here.
from goods.models import Categories, Products


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name']


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'quantity', 'price', 'discount']
    list_editable = ['price', 'discount']
    search_fields = ['name', 'description']
    list_filter = ['discount', 'price', 'category']
    fields = ['name', 'category', 'slug', 'description', 'image', ('price', 'discount'), 'quantity']
