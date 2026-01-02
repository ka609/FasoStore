from django.contrib import admin
from .models import UserProfile, Address, Notification

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at', 'updated_at')
    search_fields = ('user__username', 'phone')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'city', 'is_default', 'created_at')
    list_filter = ('country', 'city', 'is_default')
    search_fields = ('user__username', 'address', 'city', 'country')
    readonly_fields = ('created_at',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'type', 'is_read', 'created_at')
    list_filter = ('type', 'is_read')
    search_fields = ('user__username', 'message')
    readonly_fields = ('created_at',)
