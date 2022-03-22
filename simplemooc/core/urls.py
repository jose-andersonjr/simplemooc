from django.urls import include, path
from simplemooc.core import views

urlpatterns = [
    path('contato/', views.contact, name='contact'),
    path('', views.home, name='home'),
    path('anuncios/', views.anuncios, name='anuncios'),

]
