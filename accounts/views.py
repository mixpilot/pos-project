from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')


        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')


        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

         user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Account created successfully. You can now log in.")
        return redirect('login')

    return render(request, 'accounts/signup.html')