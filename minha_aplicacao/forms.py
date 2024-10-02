# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Carro  # Importe o modelo Carro do arquivo models.py
import datetime

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

class CadastroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError('A senha deve ter pelo menos 8 caracteres.')
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('As senhas não correspondem.')
        return confirm_password

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