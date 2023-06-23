from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import UserProfile
from .helpers import is_valid_password

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if (request.method == 'POST'):
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        retyped_password = request.POST['retype_password']

        if (password == retyped_password):
            valid = is_valid_password(password)
            if valid:
                if (User.objects.filter(email=email).exists()):
                    messages.error(request, 'Email already in use')
                    return redirect('register')
                elif (User.objects.filter(username=username).exists()):
                    messages.error(request, 'Username already in use')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    profile = UserProfile.objects.create(user=user, first_name=firstname, last_name=lastname)
                    profile.save()
                    return redirect('login')
            else:
                messages.error(request, 'Invalid password. Try again')
                return redirect('register')
        else: 
            messages.error(request, 'Passwords do not match. Try again')
            return redirect(request, 'register')
    else:
        return render(request, 'register.html')

def login(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            user_profile = UserProfile.objects.get(user=user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid. Try again')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')