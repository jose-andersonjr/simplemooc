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
    model = Thread
    paginate_by = 10
    template_name = 'forum/index.html'

index = ForumView.as_view()