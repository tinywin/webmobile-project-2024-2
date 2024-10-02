from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

# Função para validar o ano do carro
def validar_ano(value):
    ano_atual = date.today().year
    if value < 1886 or value > ano_atual:
        raise ValidationError(f"O ano deve estar entre 1886 e {ano_atual}")

# Função para validar o preço do carro
def validar_preco(value):
    if value <= 0:
        raise ValidationError("O preço deve ser maior que zero.")

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

    marca = models.CharField(max_length=255, choices=MARCAS_CHOICES)
    modelo = models.CharField(max_length=255)
    ano = models.IntegerField(validators=[validar_ano])  # Validação para o ano
    cor = models.CharField(max_length=255, choices=CORES_CHOICES)
    combustivel = models.CharField(max_length=255, choices=COMBUSTIVEL_CHOICES)
    quilometragem = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[validar_preco])  # Validação para o preço
    descricao = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='carros/', blank=True, null=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.ano}) - {self.cor}"