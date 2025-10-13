"""Django application configuration for the DSS module."""
from __future__ import annotations

from django.apps import AppConfig


class DssConfig(AppConfig):
    """Register the DSS app with Django."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "dss"
    verbose_name = "Onion DSS"
