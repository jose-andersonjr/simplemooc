
from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import authenticate, login, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from simplemooc.accounts.forms import RegisterForm, EditAccountForm, PasswordResetForm
from simplemooc.accounts.models import PasswordReset
from simplemooc.core.utils import generate_hash_key
from django.contrib import messages
from simplemooc.courses.models import Enrollment
# Create your views here.

User = get_user_model()

@login_required #quando a função abaixo é chamada, ele vai verificar se o user está logado, e vai executar a funcao somente se o usuário estiver logado
def dashboard(request):
    context = {}
    template_name = 'accounts/dashboard.html'
    return render(request, template_name, context)

@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user) #instance request vai verificar dados do usuario logado
        if form.is_valid():
            form.save()
            messages.success('Os dados da conta foram alterados com sucesso')
            return redirect(dashboard)
    else:
        form = EditAccountForm(instance=request.user)
    context['form'] = form
    return render(request, template_name, context)

@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)

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

def password_reset(request):
    template_name = 'accounts/password_reset.html'
    context = {}
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        form.save
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)

def password_reset_confirm(request, key):
    template_name = 'accounts/password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    return render(request, template_name, context)

