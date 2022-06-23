from re import template
from tracemalloc import get_object_traceback
from typing import ValuesView
from urllib import request
from webbrowser import get
from django.shortcuts import redirect, render, get_object_or_404, redirect

from .models import Announcement, Aula, Course, Enrollment, Materiais
from .forms import ContactCourse, FormComentario
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from simplemooc.courses import forms
from pprint import pprint
from .decorators import enrollment_required



# Create your views here.
def index(request):
    cursos = Course.objects.all()
    context = {
        'cursos' : cursos
    }
    template_name = 'courses/index.html'
    return render(request, template_name, context)

def anuncios(request):
    return render(request, 'courses/anuncios.html')

# def details(request, pk):
    curso = get_object_or_404(Course, pk=pk)
    context = {
        'curso': curso
    }
    template_name = 'courses/details.html'
    return render(request, template_name, context)

def details(request, slug):
    curso = get_object_or_404(Course, slug=slug)
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST) #request.POST aplica as respostas do formulario no no objeto form da classe ContactCourse
        if form.is_valid():
            context['is_valid'] = True
            print(form.cleaned_data['name'])
            print(form.cleaned_data['message'])
            form.send_mail(curso)
            form = ContactCourse()
            
    else:
        form = ContactCourse() #vai enviar ele em branco
    form = ContactCourse()
    context['form'] = form
    context['curso'] = curso
    template_name = 'courses/details.html'
    return render(request, template_name, context)

@login_required
def enrollment(request, slug):
    curso = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, curso=curso
    )#esse método vai pegar o usuário atual no determinado curso
    if created:
        #enrollment.active()
        messages.success(request, 'Você foi inscrito no curso com sucesso')
    else:
        messages.info(request, 'Você já está inscrito no curso')
    return redirect('dashboard')

@login_required
def undo_enrollment(request, slug):
    curso = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
        Enrollment, user=request.user, curso=curso
    )
    if request.method == 'POST':
        enrollment.delete()
        messages.info(request, 'Sua inscrição foi cancelada com sucesso')
        return redirect('dashboard')
    template = 'courses/undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'curso': curso,
    }
    return render(request, template, context)    

@login_required
@enrollment_required
def announcements(request, slug):
    curso = request.curso
    template = 'courses/announcements.html'
    context = {
        'curso': curso,
        'anuncios': curso.anuncios.all()
    }
    return render(request, template, context)


@login_required
@enrollment_required
def conteudo_anuncios(request, slug, pk): #chave primaria do anuncio
    curso = request.curso
    anuncio = get_object_or_404(curso.anuncios.all(), pk=pk)
    form = FormComentario(request.POST or None)
    print(form)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.anuncio = anuncio
        comment.save()
        form = FormComentario() 
        messages.success(request, 'Seu comentário foi enviado com sucesso')
    template = 'courses/show_announcement.html'
    anuncio = get_object_or_404(curso.anuncios.all(), pk=pk)#vai pegar todos os anuncios do curso
    context = { 
        'curso': curso,
        'anuncio': anuncio,
        'form': form,
    
    }
    return render(request, template, context) 
    
    
@login_required
@enrollment_required
def aulas(request, slug):
    curso = request.curso
    template = 'courses/aulas.html'
    aulas = curso.aulas_liberadas()
    if request.user.is_staff:
        aulas = curso.aulas.all()
    context = {
        'curso': curso,
        'aulas':aulas
    }
    return render(request, template, context)

@login_required
@enrollment_required
def aula(request, slug, pk):
    curso = request.curso
    aula = get_object_or_404(Aula, pk=pk, curso=curso)
    if not request.user.is_staff and not aula.is_available():
        messages.error(request, 'Esta aula não esta disponível')
        return redirect('aulas', slug=curso.slug)
    template = 'courses/aula.html'
    context = {
        'curso': curso,
        'aula': aula
    }
    return render(request, template, context)

@login_required
@enrollment_required
def material(request, slug, pk):
    curso = request.curso
    material = get_object_or_404(Materiais, pk=pk, aula__curso=curso)
    aula = material.aula
    if not request.user.is_staff and not aula.is_available():
        messages.error(request, 'Este material não está disponível')
        return redirect('aula', slug=curso.slug, pk=aula.pk)
    if not material.is_embutido():
        return redirect(material.file.url)
    template = 'courses/material.html'
    context = {
        'curso':curso, 
        'aula':aula,
        'material': material
    }
    return render(request, template, context)