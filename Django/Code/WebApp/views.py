from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm, ProfileForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout as auth_logout
import time
from django.shortcuts import render
from .forms import LoginForm, RegistrationForm
from Auth.models import MyUser
def Menu(request):
    start_time = time.time()
    response = render(request, 'Components/Menu.html')
    end_time = time.time()
    print(f"\n\n\n\n\nMenu view processing time: {end_time - start_time} seconds")
    return response

@login_required
def index(request):
    return render(request, 'index.html', {'user': request.user})



def login_register_view(request):
    print(request.method)
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    print("Login successful")
                    return JsonResponse({'message': 'Login successful'})
                else:
                    print("Invalid username or password")
                    return JsonResponse({'error': 'Invalid username or password'}, status=400)
            return JsonResponse({'error': 'Invalid form data'}, status=400)
        elif 'register' in request.POST:
            register_form = RegistrationForm(request.POST)
            if register_form.is_valid():
                if register_form.cleaned_data['password'] != register_form.cleaned_data['password_confirm']:
                    print("Passwords do not match")
                    return JsonResponse({'error': 'Passwords do not match'}, status=400)
                user = register_form.save(commit=False)
                user.save()
                print("Registration successful")
                return JsonResponse({'message': 'Registration successful'})
            print("Invalid form data")
            return JsonResponse({'error': 'Invalid form data'}, status=400)
    else:
        login_form = LoginForm()
        register_form = RegistrationForm()
    return render(request, 'register.html', {'login_form': login_form, 'register_form': register_form})

import os
@login_required
def getUserData(request):
    if(request.method == 'GET'):
        os.system('clear')
        user = get_user_model()
        print(request.user.getJson())
        return JsonResponse({'user': request.user.getJson()})


def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return JsonResponse({'message': 'Logout successful'})

@login_required
def edit_profile(request):
    if request.method == 'GET':
        return render(request, 'Profile.html')
    if request.method == 'POST':
        print(request.FILES)
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            print(f"File name: {uploaded_file.name}")
            print(f"File size: {uploaded_file.size} bytes")
            print(f"Content type: {uploaded_file.content_type}")
        else:
            print("No file found in the request.")
        user = request.user
        # Directly update the fields on the user object
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.about_me = request.POST.get('about_me')

        # Validate profile picture
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            valid_extensions = ['png', 'webp', 'gif']
            extension = profile_picture.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                return JsonResponse({'error': f'Unsupported file extension. Allowed extensions are: {", ".join(valid_extensions)}'}, status=400)
            user.profile_picture = profile_picture;
        
        print(f"User Object: {user.getJson()}")
        user.save()
        return JsonResponse({'message': 'Profile updated successfully!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

    
def Friends(request):
    if(request.user.is_authenticated):
        return render(request, 'Friends.html')
    return redirect('/')


# path('friendsList/', views.friends, name='friends'),


def searchUser(request):
    if request.method == 'GET':
        # Assuming you're returning a list of friends for the logged-in user
        friends = MyUser.objects.filter(userSocialCode=request.GET.get('user_code'))
        friends_data = [friend.getJson() for friend in friends]
        return JsonResponse({'friends': friends_data})
    # If the method is not GET, return an error response
    return JsonResponse({'error': 'Invalid request method'}, status=400)