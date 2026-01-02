from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('profile/', profile_view, name='profile'),

    path('addresses/', address_list_create, name='addresses'),
    path('addresses/<int:pk>/edit/', address_update, name='address_edit'),
    path('addresses/<int:pk>/delete/', address_delete, name='address_delete'),

    path('register/', register, name='register'),

    path('notifications/', notifications_list, name='notifications'),
    path('notifications/<int:pk>/read/', notification_mark_read, name='notification_read'),
    path('notifications/read-all/', notifications_mark_all_read, name='notifications_read_all'),
   path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 🔑 PASSWORD RESET
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]
