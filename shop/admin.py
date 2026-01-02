from django.contrib import admin
from .models import Category, Article, ArticleImage, Coupon

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    list_filter = ('is_active',)
    readonly_fields = ('created_at',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active', 'created_at', 'updated_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ('article', 'is_main', 'created_at')
    list_filter = ('is_main',)
    readonly_fields = ('created_at',)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'is_active', 'valid_from', 'valid_to', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('code',)
    readonly_fields = ('created_at',)
