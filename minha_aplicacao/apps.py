# apps.py
from django.apps import AppConfig

class MinhaAplicacaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'minha_aplicacao'

    def ready(self):
        import minha_aplicacao.signals  # Certifique-se de que o módulo de sinais seja importado