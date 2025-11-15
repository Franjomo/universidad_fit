from django.apps import AppConfig
from django.conf import settings
from mongoengine import connect


class FitnessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fitness'

    def ready(self):
        """
        Configure the MongoEngine connection for the fitness app.
        Uses settings.MONGO_URL and binds to alias 'fitness'.
        """
        mongo_url = getattr(settings, "MONGO_URL", None)
        if mongo_url:
            # You can reuse the same Mongo URL & DB name from MONGO_URL
            connect(host=mongo_url, alias="fitness")