from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.core import mail
from django.test.client import Client
from django.urls import reverse


class HomeViewTest(TestCase):
    client = Client()
    response = client.get('/')
    