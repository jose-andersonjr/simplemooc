from django.shortcuts import render
from .models import Course

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

