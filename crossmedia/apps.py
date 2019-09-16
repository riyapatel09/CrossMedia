from django.apps import AppConfig


class CrossmediaConfig(AppConfig):
    name = 'crossmedia'

    def ready(self):
        import crossmedia.signals
