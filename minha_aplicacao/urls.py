from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlterarSenhaView, ProfileViewSet, CarroViewSet, LoginAPI, LoginView  # Adicione LoginView aqui
from . import views

# Definindo o roteador do DRF para os ViewSets
router = DefaultRouter()
router.register(r'api/perfil', ProfileViewSet, basename='perfil')
router.register(r'api/carros', CarroViewSet, basename='carro')

urlpatterns = [
    path('entrar/', views.LoginView.as_view(), name='entrar'),  # Certifique-se que 'views' está correto
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('editar-perfil/', views.EditarPerfilView.as_view(), name='editar-perfil'),
    path('listagem/', views.ListagemView.as_view(), name='listagem'),
    path('meuperfil/', views.MeuPerfilView.as_view(), name='meuperfil'),
    path('anuncios/', views.AnunciosPublicosView.as_view(), name='anuncios_publicos'),
    path('cadastrar-carro/', views.CadastrarCarroView.as_view(), name='cadastrar-carro'), 
    path('editar-carro/<int:pk>/', views.EditarCarroView.as_view(), name='editar-carro'),
    path('remover-carro/<int:pk>/', views.RemoverCarroView.as_view(), name='remover-carro'),
    path('carro/<int:pk>/', views.DetalhesCarroView.as_view(), name='detalhes_carro'),
    path('alterar-senha/', AlterarSenhaView.as_view(), name='alterar-senha'),

    path('api/login/', LoginAPI.as_view(), name='login_api'),  # Endpoint de login da API

    path('', include(router.urls)),
]