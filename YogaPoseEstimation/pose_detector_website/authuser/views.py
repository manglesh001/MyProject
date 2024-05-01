from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from .models import User

def register(req):
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        if form.is_valid():
            email = req.POST['email']
            password = req.POST['password']
            name = email.split('@')[0]
            # if user exists
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            if user != None:
                messages.error(req, f'Invalid username or password')
                return render(req, 'authuser/register.html', {'form': form})
            # if password is not sufficient
            if len(password) < 3:
                messages.error(req, f'Invalid username or password')
                return render(req, 'authuser/register.html', {'form': form})
            user = User(email=email, name=name, password=make_password(password))
            user.save()
            login(req, user)
            return redirect('frontpage')
        else:
            messages.error(req, f'Invalid username or password')
            return render(req, 'authuser/register.html', {'form': form})
    else:
        if req.user.is_authenticated:
            return redirect('frontpage')
        form = RegisterForm()
        return render(req, 'authuser/register.html', {'form': form})


def custom_login(req):
    if req.method == 'POST':
        form = LoginForm(req.POST)
        
        if form.is_valid():
            email = req.POST['email']
            password = req.POST['password']
            # if user exists
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            if user == None:
                # messages.error(req, f'user does not exist')
                return render(req, 'authuser/login.html', {'form': form, 'custom_error': 'user does not exist'})
            if not user.check_password(password):
                # messages.error(req, f'incorrect')
                return render(req, 'authuser/login.html', {'form': form, 'custom_error': 'incorrect password entered'})
            if user:
                login(req, user)
                return redirect('frontpage')
        else:
            messages.error(req, f'Invalid username or password')
            return render(req, 'authuser/login.html', {'form': form})
    else:
        if req.user.is_authenticated:
            return redirect('frontpage')
        form = LoginForm()
        return render(req, 'authuser/login.html', {'form': form})


def sign_out(req):
    logout(req)
    return redirect('login')