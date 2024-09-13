from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweet_instance = form.save(commit=False)  # Evita conflito com o modelo Tweet
                tweet_instance.user = request.user
                tweet_instance.save()
                messages.success(request, ("Seu Tweet foi postado com sucesso!"))
                return redirect("home")
        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, "home.html", {"tweets": tweets, "form": form})
    else:
        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, "home.html", {"tweets": tweets})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, ("Você deve estar logado para visualizar esta página..."))
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        # Pegando tweets do usuário e exibindo no perfil
        tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")

        # Lógica para seguir/deixar de seguir
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST.get('follow')  # Utiliza get para evitar KeyError
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()

        return render(request, 'profile.html', {'profile': profile, 'tweets': tweets})
    else:
        messages.success(request, ("Você deve estar logado para visualizar esta página..."))
        return redirect('home')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Você entrou com sucesso no X!"))
            return redirect('home')
        else:
            messages.success(request, ("Algo deu errado com a sua entrada no X, revise o nome de usuário e a senha!"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("Você saiu com sucesso, é uma pena, é um prazer ter você aqui!"))
    return redirect('home')

# registro de usuarios

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #first_name = form.cleaned_data['first_name']
            #last_name = form.cleaned_data['last_name']
            #email = form.cleaned_data['email']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Você se registrou com sucesso!"))
            return redirect('home')
            
    return render(request, 'register.html', {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)

        # formulário de usuário

        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        
        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()

            login(request, current_user)
            messages.success(request, ("Seu perfil foi atualizado com sucesso!"))
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form, 'profile_form':profile_form})
    else:
        messages.success(request, ("Você precisa estar logado!"))
        return redirect('home')