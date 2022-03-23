from django.urls import include, path
from simplemooc.accounts import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('entrar', LoginView.as_view(), {'template_name':'registration/login.html'}, name='login'),
    path('cadastre-se', views.register, name="register"),

]