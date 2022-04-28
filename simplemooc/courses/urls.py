from django.urls import include, path, re_path
from simplemooc.courses import views

urlpatterns = [
    path('', views.index, name='index'),
    # re_path(r'^(?P<pk>\d+)/$', views.details, name='details'),
    re_path(r'^(?P<slug>[\w_-]+)/$', views.details, name='details'), #faz com que ao pesquisar o endreço refenrente a uma slug, essa slug abra o details.html do curso referido na slug
    re_path(r'^(?P<slug>[\w_-]+)/inscricao/$', views.enrollment, name='enrollment'),
    re_path(r'^(?P<slug>[\w_-]+)/cancelar-inscricao/$', views.undo_enrollment, 
        name='undo_enrollment'),
    re_path(r'^(?P<slug>[\w_-]+)/anuncios/$', views.announcements, 
        name='announcements'),
    re_path(r'^(?P<slug>[\w_-]+)/anuncios/(?P<pk>\d+)/$', views.conteudo_anuncios, #chave primaria do anuncio, o seu id
        name='conteudo_anuncios'),
    re_path(r'^(?P<slug>[\w_-]+)/aulas/$', views.aulas, name='aulas'),
    re_path(r'^(?P<slug>[\w_-]+)/aula/(?P<pk>\d+)$', views.aulas, name='aula'),
]
