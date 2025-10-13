"""Domain services for agronomic modelling.

This module contains a light-weight heuristic that will later be replaced by
calls to APSIM or AquaCrop. It is intentionally deterministic so we can build
out the rest of the system while the crop model integration is underway.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable


@dataclass(frozen=True)
class SimulationInput:
    """Normalized inputs for running a crop simulation."""

    planting_date: date
    soil_type: str
    fertilizer_plan: dict[str, float]
    irrigation_mm: float


@dataclass(frozen=True)
class SimulationResult:
    """Structured output for the simulation."""

    expected_yield_t_ha: float
    maturity_date: date
    notes: list[str]


SOIL_ADJUSTMENTS: dict[str, float] = {
    "sandy": -0.15,
    "loam": 0.0,
    "clay": 0.1,
}


FERTILIZER_FACTORS: dict[str, float] = {
    "nitrogen": 0.35,
    "phosphorus": 0.15,
    "potassium": 0.1,
}


def estimate_yield(inputs: SimulationInput) -> SimulationResult:
    """Return a deterministic yield estimate.

    The function encodes a simplified rule set that mirrors the shape of
    full-featured crop models. It uses soil modifiers, nutrient contributions,
    and irrigation adequacy to produce an expected yield.
    """

    base_yield = 12.0  # tons per hectare for reference management
    soil_modifier = SOIL_ADJUSTMENTS.get(inputs.soil_type.lower(), -0.05)

    fertilizer_effect = sum(
        FERTILIZER_FACTORS.get(name.lower(), 0.05) * amount
        for name, amount in inputs.fertilizer_plan.items()
    )

    irrigation_bonus = min(inputs.irrigation_mm / 350.0, 1.2)
    expected_yield = base_yield * (1 + soil_modifier + 0.02 * fertilizer_effect) * irrigation_bonus

    maturity_offset_days = 110 + int(10 * soil_modifier)
    maturity_date = inputs.planting_date + timedelta(days=maturity_offset_days)

    notes: list[str] = []
    if soil_modifier < -0.1:
        notes.append("Consider incorporating organic matter to improve soil water holding capacity.")
    if irrigation_bonus < 0.8:
        notes.append("Irrigation depth is below the recommended seasonal total for onions.")
    if fertilizer_effect < 1.0:
        notes.append("Fertilizer rates may limit bulb size; validate with soil tests.")

    return SimulationResult(
        expected_yield_t_ha=round(expected_yield, 2),
        maturity_date=maturity_date,
        notes=notes,
    )


def summarize_notes(notes: Iterable[str]) -> str:
    """Convert the note list to a human readable summary."""

    return "\n".join(f"• {note}" for note in notes) if notes else "Management plan looks balanced."
