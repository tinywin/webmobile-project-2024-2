from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Carro

class ProjetoTestes(TestCase):
    def setUp(self):
        # Cria um usuário para testes
        self.user = User.objects.create_user(username='usuario_teste', password='12345')
        self.client.login(username='usuario_teste', password='12345')

    # Testes do Model
    def test_criacao_carro(self):
        # Criação de um carro associado ao usuário
        carro = Carro.objects.create(
            usuario=self.user,
            marca='FORD',
            modelo='Fiesta',
            ano=2020,
            cor='PRATA',
            combustivel='FLEX',
            quilometragem=10000,
            preco=30000,
            descricao='Carro em ótimo estado'
        )
        # Verifica se o carro foi criado corretamente
        self.assertEqual(carro.modelo, 'Fiesta')
        self.assertEqual(carro.marca, 'FORD')
        self.assertEqual(carro.ano, 2020)

    # Testes da View de Cadastro
    def test_acesso_cadastro_carro(self):
        # Acessa a página de cadastro de carro
        response = self.client.get(reverse('cadastrar-carro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastrar-carro.html')

    def test_post_cadastro_carro(self):
        # Teste de POST para cadastrar um carro
        response = self.client.post(reverse('cadastrar-carro'), {
            'marca': 'FORD',
            'modelo': 'Fiesta',
            'ano': 2020,
            'cor': 'PRATA',
            'combustivel': 'FLEX',
            'quilometragem': 10000,
            'preco': 30000,
            'descricao': 'Carro em ótimo estado'
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após o cadastro

    # Testes de Login e Logout
    def test_login_usuario(self):
        # Realiza login com o usuário criado
        response = self.client.post(reverse('entrar'), {
            'username': 'usuario_teste',
            'password': '12345'
        })
        self.assertEqual(response.status_code, 302)  # Redireciona para 'home'

    def test_logout_usuario(self):
        # Realiza logout do usuário
        self.client.login(username='usuario_teste', password='12345')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redireciona para 'entrar'

    # Testes da View de Listagem de Carros
    def test_listagem_carros(self):
        # Acessa a página de listagem dos carros
        response = self.client.get(reverse('listagem'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listagem.html')