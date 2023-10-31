from django.views.generic import TemplateView
from django.shortcuts import render
from pymongo import MongoClient
from django.conf import settings
from django.shortcuts import redirect, reverse


class Index(TemplateView):
    template_name = 'index.html'


class CreateAccount(TemplateView):
    template_name = 'create_account.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        confirm_password = self.request.POST.get('confirm-password')

        mongo_client = MongoClient(settings.MONGO_URI)
        db = mongo_client.Data
        users_collection = db.UsersAccounts

        if users_collection.find_one({'email': email}):
            mongo_client.close()
            return render(request, self.template_name, {'error': 'E-mail já cadastrado', 'email': email})

        elif password != confirm_password:
            mongo_client.close()
            return render(request, self.template_name, {'error': 'As senhas são diferentes', 'email': email})

        else:
            users_collection.insert_one({'email': email, 'password': password})
            mongo_client.close()

        login_url = reverse('crypto:login') + f'?email={email}'
        return redirect(login_url)


class Login(TemplateView):
    template_name = 'login.html'

    def get(self, request):
        email = self.request.GET.get('email', '')

        return render(request, self.template_name, {'email': email})

    def post(self, request):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')

        mongo_client = MongoClient(settings.MONGO_URI)
        db = mongo_client.Data
        users_collection = db.UsersAccounts
        user = users_collection.find_one({'email': email, 'password': password})

        if user:
            mongo_client.close()
            return redirect(reverse('crypto:assets'))

        mongo_client.close()
        return render(request, self.template_name, {'error': 'E-mail não cadastrado ou senha inválida', 'email': email})


class Assets(TemplateView):
    template_name = 'assets.html'