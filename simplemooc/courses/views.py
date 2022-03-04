from django.shortcuts import render
from .models import Course
# Create your views here.
def index(request):
    cursos = Course.objects.all()
    contexto = {
        'cursos': cursos
    }
    template_name = 'courses/index.html'
    return render(request, template_name, contexto)

def anuncios(request):
    return render(request, 'courses/anuncios.html')

