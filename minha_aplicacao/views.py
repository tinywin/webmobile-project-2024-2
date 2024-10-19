from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, CadastroForm, CarroForm, EditarPerfilForm
from django.core.exceptions import ValidationError
from .models import Carro, Profile
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib import messages
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic import DetailView

class CadastroView(View):
    template_name = 'cadastro.html'

    def get(self, request):
        form = CadastroForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CadastroForm(request.POST, request.FILES)  # Suporte para upload de arquivos
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)  # Criptografa a senha
            user.save()

            if form.cleaned_data.get('foto'):
                user.profile.foto = form.cleaned_data.get('foto')
                user.profile.data_nascimento = form.cleaned_data.get('data_nascimento')
                user.profile.cpf = form.cleaned_data.get('cpf')
                user.profile.save()

            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})

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

class EditarPerfilView(View):
    template_name = 'editar-perfil.html'

    def get(self, request):
        user = request.user
        form = EditarPerfilForm(instance=user.profile)  # Usa o perfil do usuário
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user = request.user
        form = EditarPerfilForm(request.POST, request.FILES, instance=user.profile)  # Inclui request.FILES para upload de foto

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user  # Associa o perfil ao usuário
            profile.save()  # Salva o perfil

            # Atualiza os campos do usuário
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()  # Salva o usuário

            return redirect('meuperfil')  # Redireciona para o perfil após salvar

        return render(request, self.template_name, {'form': form})
    
class CadastroView(View):
    template_name = 'cadastro.html'

    def get(self, request):
        form = CadastroForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CadastroForm(request.POST, request.FILES)  # Adiciona upload de foto de perfil
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            
            if password == confirm_password:
                try:
                    user = User.objects.create_user(username, email, password)
                    login(request, user)
                    return redirect('home')
                except ValidationError as e:
                    return render(request, self.template_name, {'form': form, 'mensagem': str(e)})
            else:
                # Senhas não correspondem
                return render(request, self.template_name, {'form': form, 'mensagem': 'As senhas não correspondem.'})
        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('entrar')

class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)

class ListagemView(LoginRequiredMixin, View):
    template_name = 'listagem.html'
    login_url = reverse_lazy('entrar')

    def get(self, request):
        carros = Carro.objects.filter(usuario=request.user)  # Filtra os carros do usuário logado
        return render(request, self.template_name, {'carros': carros})

class CadastrarCarroView(View):
    template_name = 'cadastrar-carro.html'

    def get(self, request):
        form = CarroForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CarroForm(request.POST, request.FILES)
        if form.is_valid():
            carro = form.save(commit=False)
            carro.usuario = request.user  # Associa o carro ao usuário logado
            carro.save()
            messages.success(request, "Carro cadastrado com sucesso!")
            return redirect('listagem')  # Alterado para o nome correto da URL
        return render(request, self.template_name, {'form': form})
@method_decorator(login_required, name='dispatch')
class MeuPerfilView(View):
    template_name = 'meuperfil.html'

    def get(self, request):
        carros_usuario = Carro.objects.filter(usuario=request.user)  # Filtra os carros do usuário autenticado
        return render(request, self.template_name, {
            'usuario': request.user,
            'carros': carros_usuario  # Passa os carros para o template
        })

class AnunciosPublicosView(View):
    template_name = 'anuncios_publicos.html'

    def get(self, request):
        carros = Carro.objects.all()  # Busca todos os carros cadastrados
        return render(request, self.template_name, {'carros': carros})
    
class EditarCarroView(UpdateView):
    model = Carro
    fields = ['marca', 'modelo', 'ano', 'cor', 'preco', 'quilometragem', 'combustivel', 'descricao', 'foto']
    template_name = 'editar_carro.html'
    success_url = reverse_lazy('listagem')

class RemoverCarroView(DeleteView):
    model = Carro
    template_name = 'remover_carro.html'
    success_url = reverse_lazy('listagem')

class AlterarSenhaView(LoginRequiredMixin, View):
    template_name = 'alterar_senha.html'

    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantém a sessão do usuário após a troca de senha
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('meuperfil')  # Redireciona para a página do perfil
        return render(request, self.template_name, {'form': form})
    
class DetalhesCarroView(DetailView):
    model = Carro
    template_name = 'detalhes_carro.html'  # Certifique-se de que este nome está correto
    context_object_name = 'carro'