from django.urls import include, path
from simplemooc.courses import views

urlpatterns = [
    path('', views.index, name='index'),
]
