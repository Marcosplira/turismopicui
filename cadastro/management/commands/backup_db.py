from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    help = "Cria uma cópia do banco SQLite para backup local."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            default=str(settings.BASE_DIR / "backups"),
            help="Diretório onde o backup será salvo.",
        )

    def handle(self, *args, **options):
        if connection.vendor != "sqlite":
            raise CommandError(
                "Este comando local é para SQLite. Em PostgreSQL, use pg_dump."
            )

        database_path = Path(settings.DATABASES["default"]["NAME"])
        if not database_path.exists():
            raise CommandError(f"Banco não encontrado: {database_path}")

        backup_directory = Path(options["output"])
        backup_directory.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = backup_directory / f"db-{timestamp}.sqlite3"

        source = connection.connection
        if source is None:
            connection.ensure_connection()
            source = connection.connection

        destination = connection.Database.connect(backup_path)
        try:
            source.backup(destination)
        finally:
            destination.close()

        self.stdout.write(self.style.SUCCESS(f"Backup criado: {backup_path}"))
