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
    # Campos do User para serem editados no mesmo formulário
    first_name = forms.CharField(max_length=30, required=False, label='Nome')
    last_name = forms.CharField(max_length=30, required=False, label='Sobrenome')
    email = forms.EmailField(max_length=254, required=False, label='Email')

    class Meta:
        model = Profile
        fields = ['foto', 'data_nascimento', 'cpf']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EditarPerfilForm, self).__init__(*args, **kwargs)
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        # Salva o Profile
        profile = super(EditarPerfilForm, self).save(commit=False)
        if commit:
            profile.save()

        # Salva o User relacionado
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return profile