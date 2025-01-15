from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Subscriber,WaitlistedUser
from django.conf import settings



def home(request):
    if request.user.is_authenticated:  # Check if the user is already logged in
        return redirect('dashboard')  # Redirect to dashboard if logged in
    
    if request.method == "POST":
        # Distinguish the button clicked by checking `action` value
        action = request.POST.get("action")

        if action == "signin":
            email = request.POST.get("email")
            password = request.POST.get("password")
            # Check if the user exists in the database
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid email or password. Would you like to register instead?")

        elif action == "register":
            email = request.POST.get("email")
            # Check if user already exists
            if User.objects.filter(username=email).exists():
                messages.error(request, "An account with this email already exists.")
            else:
                return redirect('register')
        elif action == "newsletter":
            email = request.POST.get('email')
            if email:
                if Subscriber.objects.filter(email=email).exists():
                    messages.info(request, "You're already subscribed to the newsletter.")
                else:
                    Subscriber.objects.create(email=email)
                    messages.success(request, "Thank you for subscribing to our newsletter!")
            else:
                messages.error(request, "Please enter a valid email address.")
        else:
            messages.error(request, "Unknown action.")
    return render(request, 'home.html')  # Render the home template


def register(request):
    action = request.POST.get("action")
    
    if settings.ALLOW_NEW_USERS:
        if request.method == 'POST':
            # Handle the normal registration process here
            # Example: Create user, validate form, etc.
            # ...
            messages.success(request, 'Registration successful!')
            return redirect('home')  # Redirect after successful registration
        return render(request, 'register.html')  # Registration page
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            if action == "newsletter":
                if email:
                    if Subscriber.objects.filter(email=email).exists():
                        messages.info(request, "You're already subscribed to the newsletter.")
                    else:
                        Subscriber.objects.create(email=email)
                        messages.success(request, "Thank you for subscribing to our newsletter!")
                else:
                    messages.error(request, "Please enter a valid email address.")
            else: 
                if email:
                    # Add the email to the waitlist
                    try:
                        WaitlistedUser.objects.create(email=email)
                        messages.success(request, 'You have been added to the waitlist.')
                    except:
                        messages.error(request, 'This email is already on the waitlist.')
                else:
                    messages.error(request, 'Please provide a valid email.')
        return render(request, 'waitlist.html')  # Render waitlist form


@login_required(login_url='/')  # Redirect to home if not logged in
def dashboard(request):
    return render(request, 'dashboard.html')


def logout_user(request):
    logout(request)
    messages.success(request, "You've been logged out.")
    return redirect('home')