from django.contrib import admin
from . import models

# Register your models here.


class OrderadminInline(admin.TabularInline):
    model = models.OrderProduct
    readonly_fields = ['payment', 'user', 'product',
                       'quantity', 'product_price', 'is_ordered']
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'city',
                    'total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'phone']
    list_per_page = 20
    inlines = [OrderadminInline]


admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Payment)
admin.site.register(models.OrderProduct)
