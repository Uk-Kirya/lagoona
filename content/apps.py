from django.apps import AppConfig


class LagoonaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content'
    verbose_name = 'Контент сайта'

    def ready(self):
        import logoona.signals