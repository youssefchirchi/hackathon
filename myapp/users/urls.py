from django.urls import path
from .views import login_view, logout_view, normal_user_dashboard, welcome_page, signup_page, payment_success, payment_cancel, modele1, modele2, modele3,chatbot
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', normal_user_dashboard, name='normal_user_dashboard'),
    path('modele1/', modele1, name='modele1'),  # Add trailing slash
    path('modele2/', modele2, name='modele2'),  # Add trailing slash
    path('modele3/', modele3, name='modele3'),  # Add trailing slash

    path('', welcome_page, name='welcome'),
    path('signup/', signup_page, name='signup'),
    path('payment-success/', payment_success, name='payment_success'),
    path('payment-cancel/', payment_cancel, name='payment_cancel'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('chatbot/', chatbot, name='chatbot'),

]
