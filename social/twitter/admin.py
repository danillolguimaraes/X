from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Tweet #importando o perfil que criamos

# Removendo Groups do Painel Admin

admin.site.unregister(Group)

# Estender Modo Usuário
# tivemos que colocar class ProfileInline antes
class ProfileInline(admin.StackedInline):
  model = Profile

class UserAdmin(admin.ModelAdmin):
  model = User
  # Camos de Usuário na pagina administração
  fields = ["username"]
  #adicionando o inline que criamos
  inlines = [ProfileInline]

# cancelar o registro do usuário inicial
admin.site.unregister(User)

# Registrar novamente e Perfil
admin.site.register(User, UserAdmin)
#admin.site.register(Profile) comentamos essa seção pq não queremos duas seções distintas perfil e usuario

# Misturando profile e usuario inofrmações no admin

# class ProfileInline(admin.StackedInline):
#   model = Profile vamos ter que subir essa classe por causa da herança

# agora voltamos nos usuário que removemos os campos e deixamos o nome e vamos adicionar inlines

# registro de tweets

admin.site.register(Tweet)
