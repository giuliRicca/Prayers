from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('account/<int:user_id>/', views.account_page, name='account'),
    path('update_account/', views.update_account, name='update_account'),
    path('delete_account/', views.delete_account, name='delete_account'),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html'),
        name='reset_password'),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_send.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_form.html'),
         name='password_reset_confirm'),

    path('reset_password_complete/',
         views.password_reset_confirm,
         name='password_reset_complete'),
]
