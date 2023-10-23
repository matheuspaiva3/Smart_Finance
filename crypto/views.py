from django.shortcuts import render
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'index.html'


class CreateAccount(TemplateView):
    template_name = 'create_account.html'


class Login(TemplateView):
    template_name = 'login.html'
