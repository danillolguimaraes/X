from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
#from django.dispatch import receiver caso usassemos o receiver

# criar modelo post tweets

class Tweet(models.Model):
  user = models.ForeignKey(
      User, related_name="tweets",
      on_delete=models.DO_NOTHING   
    )
  body = models.CharField(max_length=200)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return(
      f"{self.user}"
      f"({self.created_at:%Y-%m-%d %H:%M}): "
      f"{self.body}..."
      )

# Criar o perfil de usuário

class Profile(models.Model):
  # Usuário 1 para 1 perfil, ao excluir usuário o perfil excluí em cascata
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  # SEGUIR 1 para muitos, um perfil pode seguir muitos perfis.
  # Seguidor por = followed_by usaremos de referencia, symmetrical=False vc não precisa me seguir de volta
  # blank = true, você pode ter uma conta mas não precisa seguir ninguém 
  follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)

  date_modified = models.DateTimeField(User, auto_now=True)

# toda grande mudança o servidor precisa migrar novamente python manage.py makemigrations
# feito isso precisamos empurrar nossa migração python manage.py migrate

  #adicionamos essa função para não ficar objeto no painel e sim o nome do usuário
  def __str__(self):
    return self.user.username
# criar um perfil quando um novo usuário se inscrever

#@receiver(post_save, sender=User) poderiamos usar no lugar de post_save.connect
def create_profile(sender, instance, created, **kwargs):
  if created:
    user_profile = Profile(user=instance)
    user_profile.save()
    # usuario siga a si mesmo
    user_profile.follows.set([instance.profile.id])
    user_profile.save()

post_save.connect(create_profile, sender=User)