from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
from django.utils import timezone


class UsuarioManager(BaseUserManager):
    def _create_user(self, username, email, first_name,last_name, password, is_staff, is_superuser, date_joined=None,**extra_fields):
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name = last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            date_joined = date_joined,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, first_name,last_name, password=None, **extra_fields):
        return self._create_user(username, email, first_name,last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, email, first_name,last_name, password=None, **extra_fields):
        return self._create_user(username, email, first_name,last_name, password, True, True, **extra_fields)


class User(PermissionsMixin, AbstractBaseUser):
     username = models.CharField(max_length=200, unique=True, blank=False, null=False)
     CPF = models.CharField(max_length=15, unique=True)
     email = models.CharField(max_length=100, unique=True)
     first_name = models.CharField(max_length=200, blank=True, null=True)
     last_name = models.CharField(max_length=200, blank=True, null=True)
     is_active = models.BooleanField(default=True)
     is_staff = models.BooleanField(default=False) # a admin user; non super-user
     date_joined = models.DateField(default=timezone.now)
     objects = UsuarioManager()
     USERNAME_FIELD = 'username'
     REQUIRED_FIELDS = ["email", 'nome']

     def __str__(self):
         return str(self.username)

     def has_perm(self, perm, obj=None):
         return True

     def has_module_perms(self, app_label):
         return True

class Paciente(models.Model):
    # id_paciente = models.IntergerField(primary_key=True),
    nome_paciente = models.CharField(max_length=100, null=False)
    cpf_paciente = models.CharField(max_length=14, null=False,unique=True)
    dt_nascimento = models.DateField(max_length=15)
    # user = models.ForeignKey('User',on_delete=models.CASCADE,null=False)

    def __str__(self):
        return str(self.nome_paciente)








class Impressao(models.Model):

    img = models.ImageField(upload_to='impressoes', null=True, blank=True, default='media/avatar.png')
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name='im_digital')

    def __str__(self):
        return str(self.id)

    @property
    def image_url(self):
        if self.img and hasattr(self.img, 'url'):
            return self.img.url
