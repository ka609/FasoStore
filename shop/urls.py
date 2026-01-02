from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('shop/', article_list, name='article_list'),
    path('category/<slug:slug>/', category_view, name='category'),
    path('article/<int:pk>/', article_detail, name='article_detail'),
    path('article/<int:pk>/images/', article_images, name='article_images'),
    path('search/', search_view, name='search'),
    path('coupons/', coupon_list, name='coupons'),
]
