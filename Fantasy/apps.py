from django.apps import AppConfig


class FantasyConfig(AppConfig):
    name = 'Fantasy'

    def ready(self):
        import Fantasy.signals
