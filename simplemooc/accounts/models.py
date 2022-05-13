from argparse import _MutuallyExclusiveGroup
import re
from email.policy import default
from tabnanny import verbose
from django.db.models import CASCADE
from django.db import models
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
    UserManager)
from django.conf import settings    


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'Nome de Usuário', max_length=30, unique=True,
        validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'), 
        'O nome de usuário só pode contar letras, dígitos ou os seguintes caracteres'
        ': @/./+/-/_', )]
    )
        
    email = models.CharField('E-mail', max_length=100, unique=True)
    name = models.CharField('Nome', max_length=100, blank=True)
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff =  models.BooleanField('É da equipe?', blank=True, default=False)#serve para dizer se ele pertence à parte administrativa
    date_joined = models.DateTimeField(
        'Data de entrada', auto_now_add=True #Quando o model for salvo a primeira vez o valor da data será o valor atual de data do sistema
                                                #no auto_now muda quando algum valor for atualizado
        )
    objects = UserManager()

    USERNAME_FIELD = 'username' #campo que é único e vai ser referencia na hora do login
    REQUIRED_FIELDS = ['email'] #campo que vai ser referencia na criação de superusuarios
    def __str__(self): #representação em string do usuário
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self): #vai tentar retornar o nome, se não retornar o nome, retorna o username
        return str(self) #representação em string do próprio objeto

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class PasswordReset(models.Model):
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='resets',on_delete=models.CASCADE# on_delete é obrigatório , related_name serve pra chamar o historico de reset do usuario
        
    )
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    confirmed = models.BooleanField('Confirmado?', default=False, blank=False)
    
    def __str__(self):
        return '{0} em {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        ordering = ['-created_at']