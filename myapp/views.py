from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def home(request):
    return render(request, 'home.html')
def registration(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = form.cleaned_data['full_name']
            user.save()
            messages.success(request, "Account created successfully.")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # or any other URL name
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form}) 