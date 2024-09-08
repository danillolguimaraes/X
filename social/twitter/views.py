from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm

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
