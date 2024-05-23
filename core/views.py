# Create your views here.
# views.py
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm


def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'index.html')


def contact_form(request):
    print("hello from contact_from function")
    if request.method == 'POST':
        nameText = request.POST['name']
        emailText = request.POST['email']
        subjectText = request.POST['subject']
        messageText = request.POST['message']
        print("hello from contact_from if state")

        send_mail(
            "Message From :" + subjectText,
            f"Name: {nameText}\nEmail: {emailText}\n\n{messageText}",  # E-posta gövdesi
            'your-email@example.com',  # Gönderen e-posta adresi
            ['ekinfilizatass@gmail.com'],  # Alıcı e-posta adresi
        )

        print("if worked")
        return render(request, 'index.html', {"message_name": nameText})
    else:

        print("else worked")
        return render(request, 'index.html', {"message_name": "sa"})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been logged in!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Invalid form. Please check the fields and try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have registered and logged in successfully!')
            return redirect('index')
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'register.html', context)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('index')
    else:
        form = EditProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'edit_profile.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully!')
            return redirect('index')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form': form}
    return render(request, 'change_password.html', context)


def statistics(request):
    return render(request, 'statistics.html')


def robot(request):
    user_name = request.user.username  # Assuming the user is logged in
    return render(request, 'robot.html', {'user_name': user_name})


def doctors(request):
    return render(request, 'doctors.html')


def training(request):
    return render(request, 'training.html')