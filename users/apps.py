from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import os
        if os.environ.get('RUN_MAIN') == 'true':  # Чтобы не запускалось дважды при авторелоаде
            try:
                from .models import User
                email = 'admin@admin.com'
                password = 'adminpassword123'
                if not User.objects.filter(email=email).exists():
                    User.objects.create_superuser(email=email, password=password)
                    print("Superuser created")
                else:
                    user = User.objects.get(email=email)
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()
            except Exception as e:
                print(f"Error creating superuser: {e}")
