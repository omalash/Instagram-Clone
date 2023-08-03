from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Exists, OuterRef
from .models import Profile, Post
from .helpers import is_valid_password, is_valid_email

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

        if (not username or not password or not email):
            if (not username):
                messages.error(request, 'Username is required')
            
            if (not password):
                messages.error(request, 'Password is required')

            if (not email):
                messages.error(request, 'Email is required')

            return redirect('register')

        if (password == retyped_password):
            validPassword = is_valid_password(password)
            validEmail = is_valid_email(email)
            if validPassword and validEmail:
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
                    profile = Profile.objects.create(user=user)
                    profile.save()
                    return redirect('login')
            else:
                if (not validPassword): 
                    messages.error(request, 'Invalid password. Try again')
                
                if (not validEmail): 
                    messages.error(request, 'Invalid email. Try again')

                return redirect('register')
        else: 
            messages.error(request, 'Passwords do not match. Try again')
            return redirect(request, 'register')
    else:
        return render(request, 'register.html')

def login(request):
    if (request.method == 'POST'):
        identifier = request.POST['identifier']
        password = request.POST['password']

        user = auth.authenticate(username=identifier, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Credentials Invalid. Try again')
            return redirect('login')
    else:
        return render(request, 'login.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    # Orders the created posts by newest posts
    liked_posts = Post.objects.filter(likes=request.user.profile)
    posts = profile.posts.annotate(is_liked=Exists(liked_posts.filter(pk=OuterRef('pk')))).order_by('-created_at')

    # Check if the current user is following the viewed profile
    is_following = profile.followers.filter(pk=request.user.profile.pk).exists()

    context = {
        'profile': profile, 
        'posts': posts, 
        'is_following': is_following
    }

    return render(request, 'profile.html', context)

@login_required
def create_post(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        if image:
            profile = request.user.profile
            caption = request.POST.get('caption')
            post = Post.objects.create(profile=profile, caption=caption, image=image)
            post.likes.set([])
            post.save()
            messages.success(request, "Post created successfully")
        else:
            messages.error(request, "Upload an image")
            
    return redirect('/')

@login_required
def add_like_to_post(request, post_id): 
    if request.method == 'POST':
        profile = request.user.profile
        try:
            post = Post.objects.get(pk=post_id)
            
            is_liked = profile in post.likes.all()
            if is_liked:
                post.likes.remove(profile)
            else:
                post.likes.add(profile)

            return JsonResponse({
                'success': True, 
                'likes_count': post.likes.count(),
                'is_liked': is_liked
            })
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post does not exist.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
def follow_user(request, username):
    if request.method == 'POST':
        your_user = request.user
        your_profile = your_user.profile
        try:
            other_user = User.objects.get(username=username)
            other_profile = other_user.profile
            
            is_following = your_profile.following.filter(pk=other_profile.pk).exists()
            if is_following:
                your_profile.following.remove(other_user)
                other_profile.followers.remove(your_user)
            else:
                your_profile.following.add(other_user)
                other_profile.followers.add(your_user)

            return JsonResponse({
                'success': True,
                'followers_count': other_profile.followers.count(),
                'is_following': is_following,
            }, status=200)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User does not exist.'}, status=404)
        except Profile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Profile does not exist.'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)
    

@login_required
def edit_profile(request, username):
    if request.method == "POST":
        user = request.user
        if (user.username == username):
            user.first_name = request.POST.get('new-firstname')
            user.last_name = request.POST.get('new-lastname')
            user.username = request.POST.get('new-username')
            user.save()

            profile = user.profile
            profile.description = request.POST.get('new-description')
            new_pfp = request.FILES.get('new-pfp')  
            if new_pfp:
                profile.pfp = new_pfp
            profile.save()
        else:
            return HttpResponseForbidden("You are not authorized to edit this profile.")
    
    return redirect('profile', username=user.username)

def search(request):
    search_query = request.GET.get('search_result')
    try:
        user = User.objects.get(username=search_query)
        return redirect('profile', username=user.username)
    except User.DoesNotExist:
        messages.error(request, 'User does not exist')
        return redirect('/')
    