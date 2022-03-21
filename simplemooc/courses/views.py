from webbrowser import get
from django.shortcuts import render, get_object_or_404
from .models import Course
from .forms import ContactCourse

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
    context = {'is_valid':False}
    if request.method == 'POST':
        form = ContactCourse(request.POST) #request.POST aplica as respostas do formulario no no objeto form da classe ContactCourse
        if form.is_valid():
            context['is_valid'] = True
            print(form.cleaned_data['name'])
            print(form.cleaned_data['message'])
            form = ContactCourse()
            
    else:
        form = ContactCourse() #vai enviar ele em branco
    context['form'] = form
    context['curso'] = curso
    template_name = 'courses/details.html'
    return render(request, template_name, context)

