# Generated by Django 5.1.1 on 2024-12-02 00:10

import minha_aplicacao.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minha_aplicacao', '0005_profile_telefone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cpf',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True, validators=[minha_aplicacao.models.validar_cpf]),
        ),
    ]
