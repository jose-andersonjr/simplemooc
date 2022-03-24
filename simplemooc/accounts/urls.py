from django.shortcuts import redirect
from django.urls import include, path
from simplemooc.accounts import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('entrar', LoginView.as_view(next_page='home'), name='login'),
    path('cadastre-se', views.register, name="register"),
    path('logout', LogoutView.as_view(next_page='home'), name="logout"),

]