from django.apps import AppConfig


class CourseroadConfig(AppConfig):
    name = 'courseroad'

    def ready(self):
        import courseroad.signals.handlers
