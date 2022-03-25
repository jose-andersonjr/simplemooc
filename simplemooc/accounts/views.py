from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from simplemooc.accounts.forms import RegisterForm
# Create your views here.

@login_required #quando a função abaixo é chamada, ele vai verificar se o user está logado, e vai executar a funcao somente se o usuário estiver logado
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    return render(request, template_name)
# def edit(request):
#     template_name = 'accounts/edit.html'
#     render(request, template_name)

# def edit_password(request):
#     template_name = 'accounts/edit_password.html'
#     render(request, template_name)

def register(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save() #a variável user vai receber o formulario com os dados do usuário
            user = authenticate(
                username=user.username, password=form.cleaned_data['password1']
            )#para então a função authenticate usar os usernam e o password não criptografado para fazer login
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)