from django.shortcuts import render, redirect, get_object_or_404
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
                    user.first_name = (firstname)
                    user.last_name = (lastname)
                    user.save()
                    profile = UserProfile.objects.create(user=user)
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
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid. Try again')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)
    # Pass the user and user_profile objects to the template
    return render(request, 'profile.html', {'user_profile': user_profile})