from django.apps import AppConfig


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'

class TrafficControllerConfig(AppConfig):
    name = 'traffic_controller.apps.TrafficControllerConfig'