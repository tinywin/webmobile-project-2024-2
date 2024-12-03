from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, CadastroForm, CarroForm, EditarPerfilForm
from django.core.exceptions import ValidationError
from .models import Carro, Profile
from rest_framework.generics import ListAPIView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from rest_framework.permissions import AllowAny
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib import messages
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic import DetailView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer, CarroSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Obtém o perfil do usuário logado.
        """
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['patch', 'put'])
    def update_me(self, request):
        """
        Atualiza o perfil do usuário logado.
        """
        profile = get_object_or_404(Profile, user=request.user)
        
        # Usar partial=True para permitir atualizações parciais
        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        """
        Lista todos os perfis, apenas para fins de administração ou testes.
        """
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
class CarroViewSet(viewsets.ModelViewSet):
    queryset = Carro.objects.all()
    serializer_class = CarroSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Associar carro ao usuário logado
        serializer.save(usuario=self.request.user)


class CadastroView(View):
    template_name = 'cadastro.html'

    def get(self, request):
        form = CadastroForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CadastroForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Salva o usuário e define a senha
                user = form.save(commit=False)
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()  # O sinal post_save criará o Profile automaticamente

                # Atualiza os campos adicionais no Profile
                profile = user.profile
                profile.foto = form.cleaned_data.get('foto')
                profile.data_nascimento = form.cleaned_data.get('data_nascimento')
                profile.cpf = form.cleaned_data.get('cpf')
                profile.telefone = form.cleaned_data.get('telefone')
                profile.save()

                # Login automático
                login(request, user)
                if request.user.is_authenticated:
                    messages.success(request, "Cadastro realizado com sucesso! Bem-vindo.")
                    return redirect('home')
                else:
                    messages.error(request, "Erro ao autenticar usuário após cadastro.")
            except IntegrityError as e:
                print(f"IntegrityError: {e}")  # Depuração
                messages.error(request, "Erro ao criar usuário. Verifique os dados informados.")
        else:
            print(f"Formulário inválido: {form.errors}")  # Depuração
            messages.error(request, "Erro no formulário. Verifique os campos e tente novamente.")

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
        profile, created = Profile.objects.get_or_create(user=request.user)
        form = EditarPerfilForm(instance=profile, user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
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


@method_decorator(login_required, name='dispatch')
class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)


class ListagemView(LoginRequiredMixin, View):
    template_name = 'listagem.html'
    login_url = reverse_lazy('entrar')

    def get(self, request):
        carros = Carro.objects.filter(usuario=request.user)
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


class LoginAPI(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_400_BAD_REQUEST)


class PerfilUsuarioView(View):
    template_name = 'perfil_usuario.html'

    def get(self, request, usuario_id):
        usuario = get_object_or_404(User, id=usuario_id)
        profile = get_object_or_404(Profile, user=usuario)
        anuncios = Carro.objects.filter(usuario=usuario)

        return render(request, self.template_name, {
            'usuario': usuario,
            'profile': profile,
            'anuncios': anuncios
        })


class EditarPerfilAPI(APIView):
    permission_classes = [IsAuthenticated]  # Garantir que apenas usuários autenticados possam atualizar o perfil

    def patch(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({"error": "Perfil não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        # Cria o serializer para atualizar o perfil
        serializer = ProfileSerializer(profile, data=request.data, partial=True)  # partial=True permite que apenas os campos enviados sejam atualizados
        
        if serializer.is_valid():
            serializer.save()  # Salva as alterações no perfil
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterAPI(APIView):
    """
    API para registrar novos usuários e preencher o perfil.
    """
    permission_classes = [AllowAny]  # Permitir acesso público ao endpoint

    def post(self, request):
        data = request.data

        # Verificar se o nome de usuário ou email já existem
        if User.objects.filter(username=data.get('username')).exists():
            return Response({"error": "O nome de usuário já está em uso."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=data.get('email')).exists():
            return Response({"error": "O e-mail já está em uso."}, status=status.HTTP_400_BAD_REQUEST)

        if Profile.objects.filter(cpf=data.get('cpf')).exists():
            return Response({"error": "O CPF já está em uso."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Criar o usuário
            user = User.objects.create_user(
                username=data.get('username'),
                email=data.get('email'),
                password=data.get('password'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name')
            )
            print(f"Usuário criado: {user}")

            # Atualizar os campos adicionais do perfil automaticamente criado pelo sinal
            profile = user.profile  # O sinal já criou o perfil

            # Verificar o campo 'foto'
            foto = request.FILES.get('foto', None)  # Busca em request.FILES
            profile.foto = foto  # Salva a foto (se enviada)

            profile.data_nascimento = data.get('data_nascimento')
            profile.cpf = data.get('cpf')
            profile.telefone = data.get('telefone')
            profile.save()

            # Gerar Token de autenticação
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "message": "Usuário registrado com sucesso.",
                "token": token.key,
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                },
                "profile": {
                    "data_nascimento": profile.data_nascimento,
                    "cpf": profile.cpf,
                    "telefone": profile.telefone,
                    "foto": profile.foto.url if profile.foto else None
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Erro ao registrar usuário: {e}")
            return Response({"error": f"Erro ao registrar usuário: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutAPI(APIView):
    """
    Endpoint para logout do usuário.
    """
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            # Invalida o token do usuário
            request.user.auth_token.delete()
            return Response({"message": "Logout realizado com sucesso."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Erro ao realizar logout: {e}"}, status=status.HTTP_400_BAD_REQUEST)

class EditarCarroAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        """
        Edita totalmente um carro específico do usuário.
        """
        carro = get_object_or_404(Carro, pk=pk, usuario=request.user)
        serializer = CarroSerializer(carro, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Edita parcialmente um carro específico do usuário.
        """
        carro = get_object_or_404(Carro, pk=pk, usuario=request.user)
        serializer = CarroSerializer(carro, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoverCarroAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        """
        Remove um carro específico do usuário autenticado.
        """
        carro = get_object_or_404(Carro, pk=pk, usuario=request.user)

        try:
            carro.delete()
            return Response({'message': 'Carro removido com sucesso!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Erro ao remover carro: {e}'}, status=status.HTTP_400_BAD_REQUEST)

class DetalhesCarroAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Retorna os detalhes de um carro específico.
        """
        carro = get_object_or_404(Carro, pk=pk)
        serializer = CarroSerializer(carro)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CadastrarCarroAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Cadastra um novo carro para o usuário autenticado.
        """
        serializer = CarroSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeusCarrosAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarroSerializer

    def get_queryset(self):
        """
        Retorna apenas os carros do usuário logado.
        """
        return Carro.objects.filter(usuario=self.request.user)
    
class PerfilUsuarioAPI(APIView):
    """
    API para buscar as informações de um perfil de usuário específico.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, usuario_id):
        # Busca o usuário pelo ID
        usuario = get_object_or_404(User, id=usuario_id)
        profile = get_object_or_404(Profile, user=usuario)

        # Serializa os dados do perfil
        profile_data = ProfileSerializer(profile).data

        # Busca os anúncios do usuário
        anuncios = Carro.objects.filter(usuario=usuario)
        anuncios_data = CarroSerializer(anuncios, many=True).data

        # Retorna a resposta combinada, incluindo a foto
        return Response({
            "user": {
                "id": usuario.id,
                "username": usuario.username,
                "first_name": usuario.first_name,
                "last_name": usuario.last_name,
                "email": usuario.email,
                "foto": profile.foto.url if profile.foto else None,  # Inclui o caminho completo da foto
            },
            "profile": profile_data,
            "anuncios": anuncios_data
        })