import contextlib

from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = "familybudget.users"
    verbose_name = "Users"

    def ready(self):
        with contextlib.suppress(ImportError):
            import familybudget.users.signals  # noqa: F401
