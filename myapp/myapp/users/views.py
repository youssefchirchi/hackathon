from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

from django.contrib import messages
def signup_page(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']

        # Check if password matches
        if password != password_confirmation:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('welcome')

        # Create the new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Redirect to login page after successful signup
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')
    
    return render(request, 'users/signup.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.user_type == 'doctor':
                return redirect('normal_user_dashboard')  # Redirect to doctor's dashboard
            elif user.user_type == 'normal':
                return redirect('normal_user_dashboard')  # Redirect to normal user's personal page
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def normal_user_dashboard(request):
    return render(request, 'users/normal_user_dashboard.html')

def welcome_page(request):
    return render(request, 'users/welcome.html')



