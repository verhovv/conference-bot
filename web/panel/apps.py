from django.apps import AppConfig


class PanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web.panel'

    def ready(self):
        import web.panel.signals
