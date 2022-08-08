from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView

from .models import Thread

# Create your views here
'''class ForumView(TemplateView):
    
    template_name = 'forum/index.html'
    
index = ForumView.as_view()

class ForumView(ListView):
    template_name = 'forum/indx.html'
    '''


class ForumView(ListView):

    paginate_by = 3
    template_name = 'forum/index.html'

    def get_queryset(self):
        queryset = Thread.objects.all()
        order = self.request.GET.get('get', '')
        # order = self.request.GET['order'] tem a mesma função mas na opção de cima eu posso definir o valor default caso não tenho nenhum valor
        if order == 'views':
            queryset.order_by('-views')
        elif order == 'comments':
            queryset = queryset.order_by('-answers')
        tag = self.kwargs.get('tag', '')
        if tag:
            # filtrar as tags que o slug contém
            queryset = queryset.filter(tags__slug__icontains=tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        return context


index = ForumView.as_view()
