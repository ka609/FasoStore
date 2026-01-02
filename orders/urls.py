from django.urls import path
from .views import *

urlpatterns = [
    path('checkout/', checkout_view, name='checkout'),
    path('', orders_list, name='orders_list'),
    path('<int:pk>/', order_detail, name='order_detail'),
    path('<int:pk>/pay/', payment_view, name='payment'),
    path('<int:pk>/cancel/', cancel_order, name='cancel_order'),
   path('cart/', cart_detail, name='cart'),
    path('cart/add/<int:article_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:article_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:article_id>/', update_cart_qty, name='update_cart_qty'),
]
