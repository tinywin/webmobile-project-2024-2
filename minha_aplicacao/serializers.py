from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Carro, Profile
from datetime import datetime
import re

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined']

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    date_joined = serializers.DateTimeField(source='user.date_joined', format="%d/%m/%Y %H:%M", read_only=True)

    # Foto é opcional e permitimos None
    foto = serializers.ImageField(required=False, allow_null=True)

    telefone = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'foto', 'data_nascimento', 'cpf', 'telefone']

    def update(self, instance, validated_data):
        # Atualizando os dados do User
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)
            user.save()

        # Atualizando o campo de foto apenas se ele for fornecido e válido
        if 'foto' in validated_data:
            if validated_data['foto'] is not None:
                instance.foto = validated_data['foto']
        else:
            # Não faça nada se a foto não foi enviada
            pass

        # Atualizando outros campos do Profile
        instance.data_nascimento = validated_data.get('data_nascimento', instance.data_nascimento)
        instance.cpf = validated_data.get('cpf', instance.cpf)
        instance.telefone = validated_data.get('telefone', instance.telefone)
        instance.save()
        return instance
    def validate_data_nascimento(self, value):
        """
        Permite converter datas em diferentes formatos para o padrão 'YYYY-MM-DD'.
        """
        if isinstance(value, str):
            try:
                # Tenta converter para o formato YYYY-MM-DD
                value = datetime.strptime(value.split('T')[0], '%Y-%m-%d').date()
            except ValueError:
                raise serializers.ValidationError("Formato de data inválido. Use 'YYYY-MM-DD'.")
        return value
class CarroSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)

    class Meta:
        model = Carro
        fields = [
            'id', 'usuario', 'marca', 'modelo', 'ano', 'cor', 'preco', 
            'quilometragem', 'combustivel', 'descricao', 'foto'
        ]

    def create(self, validated_data):
        # Associa automaticamente o carro ao usuário logado
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)
