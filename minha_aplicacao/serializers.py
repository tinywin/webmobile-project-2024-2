from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Carro, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'foto', 'data_nascimento', 'cpf']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            # Atualiza os campos do usuário
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)
            user.save()
        
        # Atualiza os campos do perfil
        instance.foto = validated_data.get('foto', instance.foto)
        instance.data_nascimento = validated_data.get('data_nascimento', instance.data_nascimento)
        instance.cpf = validated_data.get('cpf', instance.cpf)
        instance.save()
        return instance

class CarroSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)

    class Meta:
        model = Carro
        fields = ['id', 'usuario', 'marca', 'modelo', 'ano', 'cor', 'preco', 'quilometragem', 'combustivel', 'descricao', 'foto']
