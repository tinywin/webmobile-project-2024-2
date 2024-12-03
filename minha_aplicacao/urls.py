from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AlterarSenhaView, ProfileViewSet, CarroViewSet, LoginAPI, LogoutAPI, LoginView,
    CadastroView, HomeView, LogoutView, EditarPerfilView, ListagemView,
    MeuPerfilView, AnunciosPublicosView, CadastrarCarroAPI, EditarCarroAPI,
    RemoverCarroAPI, DetalhesCarroAPI, RegisterAPI, CadastrarCarroView, EditarCarroView,
    RemoverCarroView, MeusCarrosAPI, DetalhesCarroView, PerfilUsuarioView, PerfilUsuarioAPI
)

# Configuração do roteador do DRF
router = DefaultRouter()
router.register(r'perfil', ProfileViewSet, basename='perfil')
router.register(r'carros', CarroViewSet, basename='carro')

# Rotas do projeto
html_patterns = [
    # Autenticação
    path('entrar/', LoginView.as_view(), name='entrar'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('alterar-senha/', AlterarSenhaView.as_view(), name='alterar-senha'),

    # Páginas de navegação
    path('', HomeView.as_view(), name='home'),
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
]

api_patterns = [
    # Autenticação API
    path('register/', RegisterAPI.as_view(), name='register_api'),
    path('logout/', LogoutAPI.as_view(), name='api-logout'),
    path('login/', LoginAPI.as_view(), name='login_api'),

    # Gerenciamento de carros API
    path('cadastrar-carro/', CadastrarCarroAPI.as_view(), name='api_cadastrar_carro'),
    path('editar-carro/<int:pk>/', EditarCarroAPI.as_view(), name='api_editar_carro'),
    path('remover-carro/<int:pk>/', RemoverCarroAPI.as_view(), name='api_remover_carro'),
    path('detalhes-carro/<int:pk>/', DetalhesCarroAPI.as_view(), name='api_detalhes_carro'),
    path('carros/meus-carros/', MeusCarrosAPI.as_view(), name='api_meus_carros'),

    # Perfis de usuários API
    path('perfil-usuario/<int:usuario_id>/', PerfilUsuarioAPI.as_view(), name='perfil_usuario_api'),

    # Inclusão do roteador do DRF
    path('', include(router.urls)),
]

urlpatterns = [
    path('', include(html_patterns)),
    path('api/', include((api_patterns, 'api'), namespace='api')),
]