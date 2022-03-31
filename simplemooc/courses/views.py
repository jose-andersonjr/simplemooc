from webbrowser import get
from django.shortcuts import redirect, render, get_object_or_404, redirect
from .models import Course, Enrollment
from .forms import ContactCourse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
def announcements(request, slug):
    curso = get_object_or_404(Course, slug=slug)
    if not request.user.is_staff:
        enrollment = get_object_or_404(
            Enrollment, user=request.user, curso=curso
        )
        if not enrollment.is_approved(): #se ele não estiver aprovado
            messages.error(request, 'A sua inscrição está pendente')
            return redirect('dashboard')
    template = 'courses/announcements.html'
    context = {
        'curso': curso,
        'anuncios': curso.anuncios.all()
    }
    return render(request, template, context)