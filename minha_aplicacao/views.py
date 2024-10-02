from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, CadastroForm, CarroForm
from django.core.exceptions import ValidationError
from .models import Carro 

class LoginView(View):
    template_name = 'entrar.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                contexto = {'form': form, 'mensagem': 'Nome de usuário ou senha incorretos'}
                return render(request, self.template_name, contexto)
        return render(request, self.template_name, {'form': form})

class CadastroView(View):
    template_name = 'cadastro.html'

    def get(self, request):
        form = CadastroForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CadastroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.create_user(username, email, password)
                login(request, user)
                return redirect('home')
            except ValidationError as e:
                return render(request, self.template_name, {'form': form, 'mensagem': str(e)})
        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)

class ListagemView(View):
    template_name = 'listagem.html'

    def get(self, request):
        carros = Carro.objects.all()  # Pega todos os carros no banco de dados
        return render(request, self.template_name, {'carros': carros})

class CadastrarCarroView(View):
    template_name = 'cadastrar-carro.html'  # Certifique-se que o template existe

    def get(self, request):
        form = CarroForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CarroForm(request.POST, request.FILES)  # Adiciona suporte a upload de arquivos (fotos)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, self.template_name, {'form': form})
