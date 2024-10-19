# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Carro  # Importe o modelo Carro do arquivo models.py
import datetime
import re
from .models import Profile  # Assumindo que você tem um modelo Profile
from django.utils import timezone

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

class CadastroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Senha')
    foto = forms.ImageField(required=False, label='Foto de Perfil')
    data_nascimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Data de Nascimento')
    cpf = forms.CharField(max_length=11, label='CPF')

    class Meta:
        model = User
        fields = ['username', 'email']  # Campos que serão exibidos

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('A senha deve ter pelo menos 8 caracteres.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        data_nascimento = cleaned_data.get('data_nascimento')
        cpf = cleaned_data.get('cpf')

        # Validação da senha e confirmação de senha
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'As senhas não correspondem.')

        # Verificação de maioridade (18 anos)
        hoje = timezone.now().date()
        idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
        if idade < 18:
            self.add_error('data_nascimento', 'Você deve ser maior de 18 anos para se cadastrar.')

        # Validação simples do CPF
        if not re.match(r'^\d{11}$', cpf):
            self.add_error('cpf', 'Digite um CPF válido (11 dígitos, sem pontos ou traços).')

        return cleaned_data

class CarroForm(forms.ModelForm):
    class Meta:
        model = Carro
        fields = ['marca', 'modelo', 'ano', 'cor', 'combustivel', 'quilometragem', 'preco', 'descricao', 'foto']

    def clean_ano(self):
        ano = self.cleaned_data.get('ano')
        ano_atual = datetime.date.today().year
        if ano < 1900 or ano > ano_atual:
            raise forms.ValidationError(f"Por favor, insira um ano entre 1900 e {ano_atual}.")
        return ano

class EditarPerfilForm(forms.ModelForm):
    foto = forms.ImageField(required=False, label='Foto de Perfil')

    class Meta:
        model = Profile  # Use o modelo de perfil
        fields = ['first_name', 'last_name', 'email', 'foto'] 