from django.urls import include, path
from simplemooc.core import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('entrar', LoginView.as_view(), {'template_name':'registration/login.html'}, name='login'),

]