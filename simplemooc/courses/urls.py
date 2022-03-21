from django.urls import include, path, re_path
from simplemooc.courses import views

urlpatterns = [
    path('', views.index, name='index'),
    # re_path(r'^(?P<pk>\d+)/$', views.details, name='details'),
    re_path(r'^(?P<slug>[\w_-]+)/$', views.details, name='details'), #faz com que ao pesquisar o endreço refenrente a uma slug, essa slug abra o details.html do curso referido na slug
]
