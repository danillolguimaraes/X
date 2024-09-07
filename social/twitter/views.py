from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile

def home(request):
  return render(request, "home.html", {})


def profile_list(request):
  if request.user.is_authenticated:
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'profile_list.html', {'profiles':profiles})
  else:
    messages.success(request, ("Você deve estar logado para visualizar esta página..."))
    return redirect('home')

def profile(request, pk):
  if request.user.is_authenticated:
    profile = Profile.objects.get(user_id=pk)

    #lógica pós formulário seguir
    if request.method == "POST":
      # pegar ID atual
      current_user_profile = request.user.profile
      # pegar os dados do formulário
      action = request.POST['follow']
      # decidir seguir ou não seguir
      if action == "unfollow":
        current_user_profile.follows.remove(profile)
      elif action == "follow":
        current_user_profile.follows.add(profile)
      # salvar o perfil
      current_user_profile.save()

    return render(request, 'profile.html',{'profile':profile})
  else:
    messages.success(request, ("Você deve estar logado para visualizar esta página..."))
    return redirect('home')