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
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer, CarroSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# ViewSet para o Profile
class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def me(self, request):
        # Obter perfil do usuário logado
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def update(self, request, pk=None):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ViewSet para o Carro
class CarroViewSet(viewsets.ModelViewSet):
    queryset = Carro.objects.all()
    serializer_class = CarroSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Associar carro ao usuário logado
        serializer.save(usuario=self.request.user)

# Views Existentes
class CadastroView(View):
    template_name = 'cadastro.html'

    def get(self, request):
        form = CadastroForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CadastroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # Criação automática do perfil do usuário
            Profile.objects.create(
                user=user,
                foto=form.cleaned_data.get('foto'),
                data_nascimento=form.cleaned_data.get('data_nascimento'),
                cpf=form.cleaned_data.get('cpf')
            )

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
        # Garante que o perfil do usuário logado exista
        profile, created = Profile.objects.get_or_create(user=request.user)

        # Passa o usuário para o formulário
        form = EditarPerfilForm(instance=profile, user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # Garante que o perfil do usuário logado exista
        profile, created = Profile.objects.get_or_create(user=request.user)

        form = EditarPerfilForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('meuperfil')

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
        carros = Carro.objects.filter(usuario=request.user)  # Filtrar carros do usuário logado
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
            carro.usuario = request.user
            carro.save()
            messages.success(request, "Carro cadastrado com sucesso!")
            return redirect('listagem')
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name='dispatch')
class MeuPerfilView(DetailView):
    model = Profile
    template_name = 'meuperfil.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile

class AnunciosPublicosView(View):
    template_name = 'anuncios_publicos.html'

    def get(self, request):
        carros = Carro.objects.all()
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
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('meuperfil')
        return render(request, self.template_name, {'form': form})

class DetalhesCarroView(DetailView):
    model = Carro
    template_name = 'detalhes_carro.html'
    context_object_name = 'carro'