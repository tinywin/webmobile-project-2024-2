from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AlterarSenhaView, ProfileViewSet, CarroViewSet, LoginAPI, LoginView,
    CadastroView, HomeView, LogoutView, EditarPerfilView, ListagemView,
    MeuPerfilView, AnunciosPublicosView, CadastrarCarroView, EditarCarroView,
    RemoverCarroView, DetalhesCarroView, PerfilUsuarioView
)

# Configuração do roteador do DRF para os ViewSets
router = DefaultRouter()
router.register(r'api/perfil', ProfileViewSet, basename='perfil')
router.register(r'api/carros', CarroViewSet, basename='carro')

# Rotas do projeto
urlpatterns = [
    # Autenticação
    path('entrar/', LoginView.as_view(), name='entrar'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('alterar-senha/', AlterarSenhaView.as_view(), name='alterar-senha'),

    # Páginas de navegação
    path('', HomeView.as_view(), name='home'),  # Página inicial
    path('home/', HomeView.as_view(), name='home'),
    path('editar-perfil/', EditarPerfilView.as_view(), name='editar-perfil'),
    path('meuperfil/', MeuPerfilView.as_view(), name='meuperfil'),
    path('listagem/', ListagemView.as_view(), name='listagem'),
    path('anuncios/', AnunciosPublicosView.as_view(), name='anuncios_publicos'),

    # Gerenciamento de carros
    path('cadastrar-carro/', CadastrarCarroView.as_view(), name='cadastrar-carro'),
    path('editar-carro/<int:pk>/', EditarCarroView.as_view(), name='editar-carro'),
    path('remover-carro/<int:pk>/', RemoverCarroView.as_view(), name='remover-carro'),
    path('carro/<int:pk>/', DetalhesCarroView.as_view(), name='detalhes_carro'),

    # Perfis de usuários
    path('perfil/<int:usuario_id>/', PerfilUsuarioView.as_view(), name='perfil_usuario'),

    # API Endpoints
    path('api/login/', LoginAPI.as_view(), name='login_api'),
    path('', include(router.urls)),  # Roteador do DRF
]
