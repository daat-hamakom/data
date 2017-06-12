from django.apps import AppConfig


class MapsConfig(AppConfig):
    name = 'daat.maps'

    def ready(self):
        import daat.maps.tasks