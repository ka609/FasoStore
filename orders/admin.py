from django.contrib import admin
from .models import Cart, Delivery, Order, Payment

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    readonly_fields = ('created_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'subtotal', 'delivery_fee', 'total', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'method', 'amount', 'status', 'transaction_ref', 'created_at')
    list_filter = ('status', 'method')
    search_fields = ('order__id', 'transaction_ref')
    readonly_fields = ('created_at',)
