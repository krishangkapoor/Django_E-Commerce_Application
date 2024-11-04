from django.urls import path
from .views import register_view, login_view, logout_view, home_view, forgot_password_view, user_list, delete_user, approve_user
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', forgot_password_view, name='forgot_password'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('users/', user_list, name='user_list'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('approve_user/<int:user_id>/', approve_user, name='approve_user'),
]
