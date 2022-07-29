from doctest import master
from re import template
from tabnanny import verbose
from time import timezone
from turtle import update
from urllib import request
from django import dispatch
from django.conf import settings
from django.db import models
from django.forms import DateField
from django.urls import reverse
from django.contrib.auth import get_user_model
from simplemooc.settings import AUTH_USER_MODEL
from simplemooc.core.mail import send_mail_template
import datetime

# Create your models here.
class CourseManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | \
            models.Q(description__icontains=query)
            )  #busco um objeto do tipo queryset que vai fornecer os registros do banco da dados
                # vai fazer uma

class Course(models.Model):

    name = models.CharField('Nome', max_length=100) #a variável está a nível de programação e a string a nível de usuário
    
    slug = models.SlugField('Atalho')
    
    description = models.TextField(
        'Descrição', blank=True
        )
    
    large_description = models.TextField(
        'Sobre o curso', blank=True
    )

    start_date = models.DateField(
        'Data de Início', null=True, blank=True
        )
        
    image = models.ImageField(
        upload_to='courses/images', verbose_name='Imagem',
        null=True, blank=True
        )

    created_at = models.DateTimeField(
        'Criado em', auto_now_add=True 
        )#toda vez que um objeto curso for criado ele vai salvar a data e hora

    updated_at = models.DateTimeField(
        'Atualizado em', auto_now=True 
        )#toda vez que um objeto curso for salvo/atualizado ele vai salvar a data e hora
    
    objects = CourseManager()

    def __str__(self):
        return self.name

    class Meta: #deixar os textos mais organizados, trabalha na exibição
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name'] #['-name']

    def get_absolute_url(self):
        return reverse('details', args=[self.slug]) #essa funcão recebe envia o slug do curso em questão como parâmetro para a o arquivo details.html 
    
    def aulas_liberadas(self):
        today = datetime.date.today()
        return self.aulas.filter(release_date__lte=today)
        
class Aula(models.Model):
    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descrição', blank=True)
    numero = models.IntegerField('Número (ordem)', blank=True, default=0)
    release_date = models.DateField('Data de liberação da aula: ', blank=True, null=True)
    curso = models.ForeignKey(Course, verbose_name="Curso", related_name="aulas", on_delete=models.CASCADE)
    created_at = models.DateTimeField('Criado em:', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em:', auto_now=True)
    
    def __str__(self):
        return self.nome
    
    def is_available(self):
        if self.release_date:
            today = datetime.date.today()
            return self.release_date <= today
        return False
    
    class Meta:
        
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"
        ordering = ['numero']
        
class Materiais(models.Model):
    
    nome = models.CharField('Nome', max_length=100)
    embutido = models.TextField('Vídeo embutido', blank=True)
    arquivo = models.FileField(upload_to='aulas/materiais', blank=True, null=True)
    
    aula = models.ForeignKey(Aula, verbose_name='Aula', related_name='material', on_delete=models.CASCADE)
    
    def is_embutido(self):
        return bool(self.embutido)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'
        
        
    
class Enrollment(models.Model):
    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name='Usuário', 
        related_name='usuarios', on_delete=models.CASCADE
    )
    curso = models.ForeignKey(
        Course, verbose_name='Curso', related_name='enrollments',
        on_delete=models.CASCADE
    )
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=0, blank=True
    )
    created_at = models.DateTimeField('Criado em:', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em:', auto_now=True)
    
    def active(self):
        self.status = 1
        self.save()
    
    def is_approved(self):
        return self.status == 1
    
    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user', 'curso'),) #índice de unicidade, so pode existir um usuario e um curso juntos, ou seja, se vc esta em um curso nao pdoe se inscrever de novo 
        
class Announcement(models.Model):
    curso = models.ForeignKey(Course, verbose_name='Curso', on_delete=models.CASCADE, related_name='anuncios')
    titulo = models.CharField('Título', max_length=100)
    content = models.TextField('Conteúdo')
    created_at = models.DateTimeField('Criado em:', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em:', auto_now=True)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-created_at']
        
class Comment(models.Model):
    announcement = models.ForeignKey(
        Announcement, verbose_name='Anúncio', on_delete=models.CASCADE, related_name='comments'
        )
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuário") #quando o usuário for deletado do sistema todas as suas tarefas sao apagadas - on_delete=CASCADE
    comment = models.TextField('Comentário')
    created_at = models.DateTimeField('Criado em:', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em:', auto_now=True)
    
    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']
        
def post_save_announcement(instance, created, **kwargs):
    if created:
        subject = instance.titulo
        context = {
            'announcement': instance
        }
        template_name = 'courses/instance_mail.html'
        for inscricao in Enrollment.objects.filter(curso=instance.curso, status=1):
            recipient_list = [inscricao.user.email] 
            send_mail_template(subject, template_name, context, recipient_list)
            
models.signals.post_save.connect(
    post_save_announcement, sender=Announcement, 
    dispatch_uid='post_save_announcement' #verifica se a função já está cadastrada
    )

