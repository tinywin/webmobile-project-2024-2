from django.db import IntegrityError, models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from datetime import date
import re

# Validação do ano do carro
def validar_ano(value):
    ano_atual = date.today().year
    if value < 1886 or value > ano_atual:
        raise ValidationError(f"O ano deve estar entre 1886 e {ano_atual}.")

# Validação do preço do carro
def validar_preco(value):
    if value <= 0:
        raise ValidationError("O preço deve ser maior que zero.")

# Validação básica de CPF (11 dígitos)
def validar_cpf(value):
    if not re.fullmatch(r'\d{11}', value):
        raise ValidationError("O CPF deve conter exatamente 11 dígitos.")

class Carro(models.Model):
    # Opções de marca
    MARCAS_CHOICES = [
        ('FORD', 'Ford'),
        ('CHEVROLET', 'Chevrolet'),
        ('FIAT', 'Fiat'),
        ('VOLKSWAGEN', 'Volkswagen'),
        ('HYUNDAI', 'Hyundai'),
        ('HONDA', 'Honda'),
        ('TOYOTA', 'Toyota'),
        ('RENAULT', 'Renault'),
        ('NISSAN', 'Nissan'),
        ('JEEP', 'Jeep'),
        ('PEUGEOT', 'Peugeot'),
        ('CITROEN', 'Citroën'),
        ('MITSUBISHI', 'Mitsubishi'),
        ('BMW', 'BMW'),
        ('MERCEDES', 'Mercedes-Benz'),
        ('AUDI', 'Audi'),
        ('KIA', 'Kia'),
        ('LANDROVER', 'Land Rover'),
        ('VOLVO', 'Volvo'),
        ('CHERY', 'Chery'),
    ]

    # Opções de cor
    CORES_CHOICES = [
        ('PRETO', 'Preto'),
        ('BRANCO', 'Branco'),
        ('PRATA', 'Prata'),
        ('CINZA', 'Cinza'),
        ('VERMELHO', 'Vermelho'),
        ('AZUL', 'Azul'),
        ('VERDE', 'Verde'),
    ]

    # Opções de combustível
    COMBUSTIVEL_CHOICES = [
        ('GASOLINA', 'Gasolina'),
        ('ALCOOL', 'Álcool'),
        ('DIESEL', 'Diesel'),
        ('FLEX', 'Flex'),
        ('ELETRICO', 'Elétrico'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona com o User
    marca = models.CharField(max_length=255, choices=MARCAS_CHOICES)
    modelo = models.CharField(max_length=255)
    ano = models.IntegerField(validators=[validar_ano])
    cor = models.CharField(max_length=255, choices=CORES_CHOICES)
    combustivel = models.CharField(max_length=255, choices=COMBUSTIVEL_CHOICES)
    quilometragem = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[validar_preco])
    descricao = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='carros/', blank=True, null=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.ano}) - {self.cor}"

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    telefone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="O número de telefone deve estar no formato '+999999999'. Até 15 dígitos são permitidos."
            )
        ]
    )

    def __str__(self):
        return f"{self.user.username} Profile"
