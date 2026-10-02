import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.password_validation import validate_password


class Command(BaseCommand):
    help = "Creates or resets the configured production superuser."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_BOOTSTRAP_ADMIN_USERNAME", "").strip()
        password = os.environ.get("DJANGO_BOOTSTRAP_ADMIN_PASSWORD", "")
        email = os.environ.get("DJANGO_BOOTSTRAP_ADMIN_EMAIL", "").strip()

        if not username and not password:
            self.stdout.write("Admin bootstrap skipped; no credentials configured.")
            return

        if not password:
            raise CommandError("Set DJANGO_BOOTSTRAP_ADMIN_PASSWORD.")

        username = username or "adminturismo"

        User = get_user_model()
        usuario = User.objects.filter(username=username).first()
        if usuario and not (usuario.is_staff and usuario.is_superuser):
            raise CommandError(
                "The configured username already belongs to a non-admin user."
            )

        if usuario is None:
            validate_password(password)
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write("Production superuser created.")
            return

        if not usuario.check_password(password):
            validate_password(password, user=usuario)
            usuario.set_password(password)
            if email:
                usuario.email = email
                usuario.save(update_fields=["password", "email"])
            else:
                usuario.save(update_fields=["password"])

        self.stdout.write("Production superuser is ready.")