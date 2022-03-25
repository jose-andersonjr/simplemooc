from django.shortcuts import redirect
from django.urls import include, path
from simplemooc.accounts import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('editar', views.edit, name='edit'),
    path('editar-senha', views.edit_password, name='edit_password'),
    path('entrar', LoginView.as_view(next_page='home'), name='login'),
    path('cadastre-se', views.register, name="register"),
    path('logout', LogoutView.as_view(next_page='home'), name="logout"),
    

]