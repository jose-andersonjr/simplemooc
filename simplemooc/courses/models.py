from turtle import update
from django.db import models
from django.forms import DateField

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
