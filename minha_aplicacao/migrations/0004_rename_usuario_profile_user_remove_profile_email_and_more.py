# Generated by Django 5.1.1 on 2024-10-23 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minha_aplicacao', '0003_alter_carro_ano_alter_carro_preco_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='usuario',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
    ]