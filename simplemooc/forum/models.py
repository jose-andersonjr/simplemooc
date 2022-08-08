from tabnanny import verbose
from tkinter import CASCADE
from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings


class Thread(models.Model):  # Tópico do forum

    titulo = models.CharField('Título', max_length=100)
    corpo = models.TextField('Mensagem')
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Autor', related_name='threads', on_delete=models.CASCADE
    )
    views = models.IntegerField('Visualizações', blank=True, default=0)
    answers = models.IntegerField('Respostas', blank=True, default=0)

    tags = TaggableManager()
    created = models.DateTimeField('Criado em:', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-modified']


class Reply(models.Model):  # Respostas dos usuários
    thread = models.ForeignKey(
        Thread, verbose_name='Tópico', related_name='replies', default='', on_delete=models.CASCADE
    )
    reply = models.TextField('Resposta')
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Autor', related_name='replies', on_delete=models.CASCADE
    )

    correct = models.BooleanField('Correta?', blank=True, default=False)
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self):
        return self.reply[:100]

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-correct', 'created']
