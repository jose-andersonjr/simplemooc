from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from simplemooc.accounts.models import PasswordReset
from simplemooc.core.utils import generate_hash_key
from simplemooc.core.mail import send_mail_template

User = get_user_model()

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError(
            'Nenhum usuário encontrado com este e-mail'
        )    
        
    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        template_name = 'accounts/password_reset_mail.html'
        subject = 'Criar nova senha no simplemooc'
        context = {
            'reset':reset,
        }
        send_mail_template(subject, template_name, context, recipient_list, 
    from_email=settings.DEFAULT_FROM_EMAIL, fail_silently=False)
        



class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmação de senha:', widget=forms.PasswordInput
        )

    def clean_email(self): #função de validação do email, tambem pode ser usado para alguma manipulação no valor
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe um usuário com esse e-mail')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError(
                'A confirmação não está correta'
            )
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class EditAccountForm(forms.ModelForm): #modelform vai gerar um dicionario a partir dos campos que o modelo ja tem
    def clean_email(self): #função de validação do email, tambem pode ser usado para alguma manipulação no valor
        email = self.cleaned_data['email']
        queryset = User.objects.filter(
            email=email).exclude(pk=self.instance.pk).exists()#variavel instance remete a instancia que esta sendo alterada no momento
        if queryset:
            raise forms.ValidationError('Já existe um usuário com esse e-mail')
        return email
    
    class Meta:
        model = User #e o model que ele recebera pra fazer o fomr vai ser o User
        fields = ['username', 'email'] #os campos que queremos que o formulario pode alterar
    