from multiprocessing.connection import Client
from unicodedata import name
from venv import create
from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings
from simplemooc.courses.models import Course




class ContactCourseTestCase(TestCase):
    def setUp(self):
        self.curso = Course.objects.create(name='Django', slug='django')
        
    def tearDown(self):
        self.curso.delete()
        
    @classmethod    
    def setUpClass(cls):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
        
    def test_contact_form_error(self):
        dados = {'nome': 'Fulano de Tal', 'email': '', 'message':''}
        client = Client()
        path = reverse('details', args=[self.curso.slug])
        response = client.post(path)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')
        
    def test_contact_form_success(self):
        dados = {'nome': 'Fulano de Tal', 'email': 'admin@admin.com', 'message':'oiii'}
        client = Client()
        path = reverse('details', args=[self.curso.slug])
        response = client.post(path, dados)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL]) #A FUNÇÃO .to REPASSA UMA LISTA