from django.contrib import admin
from .models import Item, Order


# admin.site.register(Item)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'normalize_price', 'price')
    search_fields = ('name', 'description','price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','display_items', 'amount_rub', 'total_amount')