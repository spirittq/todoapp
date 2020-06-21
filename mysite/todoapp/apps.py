from django.apps import AppConfig


class TodoappConfig(AppConfig):
    name = 'todoapp'

    def ready(self):
        from .signals import create_profile, save_profile
