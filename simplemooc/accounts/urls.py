from django.shortcuts import redirect
from django.urls import include, path, re_path
from simplemooc.accounts import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('editar', views.edit, name='edit'),
    path('editar-senha', views.edit_password, name='edit_password'),
    path('entrar', LoginView.as_view(next_page='home'), name='login'),
    path('cadastre-se', views.register, name="register"),
    path('resetar-senha', views.password_reset, name="password_reset"),
    re_path(r'^nova-senha/(?P<key>\w+)/$', views.password_reset_confirm, name="password_reset_confirm"), #view do django
    path('logout', LogoutView.as_view(next_page='home'), name="logout"),

]