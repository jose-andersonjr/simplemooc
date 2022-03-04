from django.shortcuts import render
from django.http import HttpResponse

#create your viewes here

def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def anuncios(request):
    return render(request, 'anuncios.html')
