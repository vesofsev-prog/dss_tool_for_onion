"""Data models for future simulation storage.

The initial implementation keeps the schema simple. As the DSS evolves we can
persist simulation runs and agronomic parameters here.
"""
from __future__ import annotations

from django.db import models


class SimulationRecord(models.Model):
    """Minimal placeholder model for storing simulation metadata."""

    created_at = models.DateTimeField(auto_now_add=True)
    crop = models.CharField(max_length=32, default="onion")
    planting_date = models.DateField()
    soil_type = models.CharField(max_length=64)
    fertilizer_plan = models.JSONField(default=dict)
    yield_prediction = models.FloatField(help_text="Expected yield in tons per hectare")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.crop} simulation on {self.planting_date:%Y-%m-%d}"
