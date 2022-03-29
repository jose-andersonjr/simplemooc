from turtle import update
from django.conf import settings
from django.db import models
from django.forms import DateField
from django.urls import reverse

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
    
class Enrollment(models.Model):
    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário', 
        related_name='enrollments', on_delete=models.CASCADE
    )
    curso = models.ForeignKey(
        Course, verbose_name='Curso', related_name='enrollments',
        on_delete=models.CASCADE
    )
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=0, blank=True
    )
    created_at = models.DateTimeField('Criado em:', auto_now_add=True)
    update_at = models.DateTimeField('Atualizado em:', auto_now=True)
    
    
    
    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user', 'curso'),) #índice de unicidade, so pode existir um usuario e um curso juntos, ou seja, se vc esta em um curso nao pdoe se inscrever de novo 