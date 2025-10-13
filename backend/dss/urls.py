"""URL routing for DSS-specific endpoints."""
from __future__ import annotations

from django.urls import path

from . import views

app_name = "dss"

urlpatterns = [
    path("simulations/run", views.run_simulation, name="run-simulation"),
    path("simulations/presets", views.list_presets, name="list-presets"),
]
