from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Carro, Profile
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    telefone = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'foto', 'data_nascimento', 'cpf', 'telefone']

    def validate_telefone(self, value):
        if value and not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError("O número de telefone deve estar no formato '+999999999'.")
        return value

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            # Atualiza os campos do modelo User relacionado
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)
            user.save()
        
        # Atualiza os campos do modelo Profile
        instance.foto = validated_data.get('foto', instance.foto)
        instance.data_nascimento = validated_data.get('data_nascimento', instance.data_nascimento)
        instance.cpf = validated_data.get('cpf', instance.cpf)
        instance.telefone = validated_data.get('telefone', instance.telefone)
        instance.save()
        return instance


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
