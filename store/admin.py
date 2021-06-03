from django.contrib import admin
from .models import Products

# Register your models here.

@admin.register(Products)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ('product_name','price','stock','is_avilable','modified_date')
    search_fields =('product_name',)
    list_filter = ('is_avilable',)
    list_editable = ('is_avilable',)

