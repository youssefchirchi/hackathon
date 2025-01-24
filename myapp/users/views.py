import paypalrestsdk
from paypalrestsdk import Payment
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

# PayPal Configuration
paypalrestsdk.configure({
    "mode": "sandbox",  # Use "live" for production
    "client_id": "AV0xdA0cbp9neWw0KnKBE6gWnvz9ErofFU8q20h8XwLYpV2MpUQAQs9IvMaaz5XDxIsBlfUp2P6-dnCj",  # Replace with your actual PayPal Client ID
    "client_secret": "ECmWfIPx8A-Nii3GuKGF8s4u44s70IRz6grvRaEYboxJcVRLimcgQXh-c3_PLCwKr-_kbkU7pkv6Jo90"  # Replace with your actual PayPal Client Secret
})

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
            return redirect('signup')

        # Create PayPal payment
        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri('/payment-success/'),
                "cancel_url": request.build_absolute_uri('/payment-cancel/')
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Account Signup",
                        "sku": "signup_fee",
                        "price": "10.00",
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": "10.00",
                    "currency": "USD"
                },
                "description": "Account signup fee."
            }]
        })

        if payment.create():
            # Find the approval URL and redirect user to PayPal
            approval_url = next(link.href for link in payment.links if link.rel == "approval_url")
            
            # Store signup data in session to retrieve after payment approval
            request.session['signup_data'] = {
                'username': username,
                'email': email,
                'password': password
            }
            
            return redirect(approval_url)
        else:
            messages.error(request, "An error occurred while creating the payment.")
            return redirect('signup')

    return render(request, 'users/signup.html')

def payment_success(request):
    # Retrieve signup data from session
    signup_data = request.session.get('signup_data')

    if not signup_data:
        messages.error(request, "No signup data found.")
        return redirect('signup')

    # Finalize user creation
    user = User.objects.create_user(
        username=signup_data['username'],
        email=signup_data['email'],
        password=signup_data['password']
    )
    user.save()

    # Clear session data
    del request.session['signup_data']
    messages.success(request, "Payment successful! Account created. Please log in.")
    return redirect('login')

def payment_cancel(request):
    messages.error(request, "Payment was canceled.")
    return redirect('signup')




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


def modele1(request):
    return render(request, 'users/modele1.html')

def modele2(request):
    return render(request, 'users/modele2.html')

def modele3(request):
    return render(request, 'users/modele3.html')









import json
from django.shortcuts import render

def load_chatbot_data():
    try:
        with open('C:/Users/mhgui/Downloads/chatbot.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def chatbot(request):
    chatbot_data = load_chatbot_data()
    # Convert data to JSON string for JavaScript
    chatbot_data_json = json.dumps(chatbot_data)
    return render(request, 'users/chatbot.html', {'chatbot_data': chatbot_data_json})