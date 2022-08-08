from django.urls import path, include, re_path
from simplemooc.forum import views

urlpatterns = [
    path('', views.index, name='index'),
    # para casos em que o caminho vai receber uma string vazia '' devemos utilziar * ao inves de +
    re_path(r'^tag/(?P<tag>[\w_-]*)/$',
            views.index, name='index_tagged'),
]
# sempre usar re_path para expressoes regulares
