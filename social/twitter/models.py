from django.db import models
from django.contrib.auth.models import User

# Criar o perfil de usuário

class Profile(models.Model):
  # Usuário 1 para 1 perfil, ao excluir usuário o perfil excluí em cascata
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  # SEGUIR 1 para muitos, um perfil pode seguir muitos perfis.
  # Seguidor por = followed_by usaremos de referencia, symmetrical=False vc não precisa me seguir de volta
  # blank = true, você pode ter uma conta mas não precisa seguir ninguém 
  follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)

# toda grande mudança o servidor precisa migrar novamente python manage.py makemigrations
# feito isso precisamos empurrar nossa migração python manage.py migrate

  #adicionamos essa função para não ficar objeto no painel e sim o nome do usuário
  def __str__(self):
    return self.user.username