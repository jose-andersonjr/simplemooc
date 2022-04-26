from cProfile import label
from dataclasses import field
from django import forms
from django.core.mail import send_mail
from django.conf import settings
from simplemooc.settings import CONTACT_EMAIL
from simplemooc.core.mail import send_mail_template
from .models import Comment


class ContactCourse(forms.Form):

    name = forms.CharField(
        label="Nome", max_length=100
        )
    email = forms.EmailField(
        label="E-mail"
        )
    message = forms.CharField(
        label="Mensagem/Dúvida", widget=forms.Textarea
        )#colocando a opção required=false os campos deixam de ser obrigatorios

    def send_mail(self, curso):
        subject = 'Contato Curso sobre o curso [%s]' % curso
        message = 'Nome: %(name)s; E-mail: %(email)s; Mensage:%(message)s'
        context = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message']

        }
        template_name = 'courses/contact_email.html'
        send_mail_template(
            subject, template_name, context, [settings.CONTACT_EMAIL], 
        )
        
class FormComentario(forms.ModelForm):
    class Meta:
        model = Comment
        field = ['comentario']
        exclude = ()