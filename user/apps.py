from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError
from decouple import config

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        try:
            User = get_user_model()
            admin_username = config("ADMIN_USERNAME", default="admin")
            admin_password = config("ADMIN_PASSWORD", default="admin123")

            if not User.objects.filter(username=admin_username).exists():
                User.objects.create_superuser(
                    username=admin_username,
                    password=admin_password,
                    email="admin@example.com",
                    role="admin"
                )
                print("✅ Admin user created.")
        except (OperationalError, ProgrammingError):
            # Happens during `makemigrations` or `migrate`
            pass
