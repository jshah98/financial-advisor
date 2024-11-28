from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def home(request):
    if request.user.is_authenticated:  # Check if the user is already logged in
        return redirect('dashboard')  # Redirect to dashboard if logged in
    
    if request.method == "POST":  # Handle form submission
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Check if the user exists in the database
        if User.objects.filter(username=email).exists():
            # User exists, try to authenticate
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)  # Log the user in
                return redirect('dashboard')  # Redirect to the dashboard
            else:
                messages.error(request, "Invalid username and password.")  # User exists but invalid password
        else:
            # User does not exist, try to register
            try:
                # Use the email as the username
                user = User.objects.create_user(username=email, email=email, password=password)
                print('here')
                login(request, user)  # Log the user in after registration
                messages.success(request, "Registration successful! Logged in.")
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f"Error during registration: {str(e)}")  # Handle registration error

    return render(request, 'home.html')  # Render the home template

@login_required(login_url='/')  # Redirect to home if not logged in
def dashboard(request):
    return render(request, 'dashboard.html')


def logout_user(request):
    logout(request)
    messages.success(request, "You've been logged out.")
    return redirect('home')