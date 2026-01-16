from django.apps import AppConfig
import os


class NewappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newapp'

    def ready(self):
        if os.environ.get("CREATE_SUPERUSER") == "true":
            from django.contrib.auth import get_user_model
            User = get_user_model()

            username = os.environ.get("DJANGO_SU_NAME")
            email = os.environ.get("DJANGO_SU_EMAIL")
            password = os.environ.get("DJANGO_SU_PASSWORD")

            if username and password:
                if not User.objects.filter(username=username).exists():
                    User.objects.create_superuser(
                        username=username,
                        email=email,
                        password=password
                    )

