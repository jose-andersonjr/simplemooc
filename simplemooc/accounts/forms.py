from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):

    email = forms.EmailField(label='E-mail')

    def clean_email(self): #função de validação do email, tambem pode ser usado para alguma manipulação no valor
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe um usuário com esse e-mail')
        return email
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
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
        fields = ['username', 'email', 'first_name', 'last_name'] #os campos que queremos que o formulario pode alterar
    