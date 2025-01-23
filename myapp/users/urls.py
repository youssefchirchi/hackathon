from django.urls import path
from .views import login_view, logout_view, normal_user_dashboard,welcome_page,signup_page

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', normal_user_dashboard, name='normal_user_dashboard'),  # Add this line
    path('', welcome_page, name='welcome'),
    path('signup/',signup_page, name='signup'), 
]
