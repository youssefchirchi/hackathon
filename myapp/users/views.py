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





from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import torch
from PIL import Image, ImageOps
import torchvision.transforms as transforms

def predict_image_class_1(image_path, model_path=r"C:\Users\mhgui\Downloads\hackathon-main\hackathon-main\myapp\users\trained_model_full.pth", class_labels=None):
    """
    Predicts the class of an image using a pre-trained model.
    """
    # Load the model
    model = torch.load(model_path, weights_only=False)
    model.eval()

    # Load and preprocess the image
    image = Image.open(image_path).convert("RGB")
    image = ImageOps.grayscale(image)

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])

    input_image = transform(image).unsqueeze(0)

    # Perform prediction
    with torch.no_grad():
        output = model(input_image)

    _, predicted_class = torch.max(output, 1)

    # Define default class labels if not provided
    if class_labels is None:
        class_labels = ['AbdomenCT', 'BreastMRI', 'ChestCT', 'CXR', 'HeadCT', 'Hand']

    predicted_label = class_labels[predicted_class.item()]
    return predicted_label


def modele1(request):
    """
    Handles the image upload, predicts its class, and renders the result.
    """
    if request.method == 'POST' and request.FILES['image']:
        uploaded_file = request.FILES['image']

        # Save the uploaded file to the media folder
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)

        # Get the absolute file path for processing
        image_path = fs.path(filename)  # Absolute path for the file
        file_url = fs.url(filename)  # URL to display the file in the template

        # Predict the class of the uploaded image
        predicted_label = predict_image_class_1(image_path)

        return render(request, 'users/modele1.html', {
            'file_url': file_url,
            'predicted_label': predicted_label
        })

    return render(request, 'users/modele1.html')







from transformers import pipeline

def summarize_text(text_file_path, model_path=None, max_length=130, min_length=30, do_sample=False):
    """
    Summarizes the text from a file using a pre-trained model.
    """
    # Load summarization pipeline
    summarizer = pipeline("summarization", model=model_path) if model_path else pipeline("summarization")

    # Read text from the file
    with open(text_file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Perform summarization
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=do_sample)

    # Extract and return the summary text
    return summary[0]['summary_text']



def modele2(request):
    """
    Handles the file upload, summarizes its content, and renders the result.
    """
    if request.method == 'POST' and request.FILES['text_file']:
        uploaded_file = request.FILES['text_file']

        # Save the uploaded file to the media folder
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)

        # Get the absolute file path for processing
        file_path = fs.path(filename)  # Absolute path for the file
        file_url = fs.url(filename)  # URL to display the file in the template

        # Summarize the text from the uploaded file
        summary = summarize_text(file_path)

        return render(request, 'users/modele2.html', {
            'file_url': file_url,
            'summary': summary
        })

    return render(request, 'users/modele2.html')





# views.py
from django.http import JsonResponse
from django.shortcuts import render
import requests
import json

def chatbot(request):
    return render(request, "users/chatbot.html")

def send_message(request):
    if request.method == "POST":
        message = request.POST.get("message")
        
        # Détails de l'API Langflow
        BASE_API_URL = "http://127.0.0.1:7860"
        FLOW_ID = "726f22c1-ad7e-468f-9acf-3ce5be9fb608"
        ENDPOINT = f"{BASE_API_URL}/api/v1/run/{FLOW_ID}"

        # Corps de la requête
        payload = {
            "input_value": message,
            "output_type": "chat",
            "input_type": "chat"
        }

        try:
            response = requests.post(ENDPOINT, json=payload)
            response_data = response.json()

            # Extraction du texte de la réponse
            reply = response_data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            return JsonResponse({"reply": reply})
        except Exception as e:
            return JsonResponse({"reply": "Une erreur s'est produite lors du traitement de votre message."})

    return JsonResponse({"reply": "Invalid request."})













import json
import requests
from django.http import JsonResponse
from django.shortcuts import render

BASE_API_URL = "http://127.0.0.1:7860"
FLOW_ID = "e4c85067-e768-4e5f-9919-7a8d414265bc"

def run_flow(message: str):
    """
    Appelle l'API LangFlow et récupère la réponse.
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{FLOW_ID}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def modele3(request):
    """
    Gère les requêtes pour le chatbot.
    """
    if request.method == "POST":
        message = request.POST.get("message")
        if message:
            api_response = run_flow(message)
            result = (
                api_response.get("outputs", [{}])[0]
                .get("outputs", [{}])[0]
                .get("results", {})
                .get("message", {})
                .get("text", "Erreur dans la réponse.")
            )
            return JsonResponse({"response": result})
    return render(request, "users/modele3.html")
