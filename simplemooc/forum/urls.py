from django.urls import path, include
from simplemooc.forum import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.index, name='index_tagged')
]
