"""HTTP views that expose the simulation functionality."""
from __future__ import annotations

import json
from datetime import date

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .services import SimulationInput, estimate_yield, summarize_notes

PRESET_SCENARIOS = [
    {
        "name": "Dry season - irrigated",
        "planting_date": "2025-11-15",
        "soil_type": "loam",
        "irrigation_mm": 420,
        "fertilizer_plan": {"nitrogen": 1.2, "phosphorus": 0.6, "potassium": 0.8},
    },
    {
        "name": "Wet season - rainfed",
        "planting_date": "2025-06-01",
        "soil_type": "sandy",
        "irrigation_mm": 250,
        "fertilizer_plan": {"nitrogen": 0.8, "phosphorus": 0.5, "potassium": 0.4},
    },
]


def list_presets(_request: HttpRequest) -> JsonResponse:
    """Return presets that the front-end can use for quick exploration."""

    return JsonResponse({"presets": PRESET_SCENARIOS})


@csrf_exempt
def run_simulation(request: HttpRequest) -> JsonResponse:
    """Handle POST requests from the front-end to run a simulation."""

    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"detail": "Invalid JSON payload"}, status=400)

    try:
        inputs = SimulationInput(
            planting_date=date.fromisoformat(payload["planting_date"]),
            soil_type=payload["soil_type"],
            irrigation_mm=float(payload.get("irrigation_mm", 0)),
            fertilizer_plan={
                name: float(amount) for name, amount in payload.get("fertilizer_plan", {}).items()
            },
        )
    except (KeyError, ValueError) as exc:
        return JsonResponse({"detail": f"Invalid input: {exc}"}, status=400)

    result = estimate_yield(inputs)

    return JsonResponse(
        {
            "expected_yield_t_ha": result.expected_yield_t_ha,
            "maturity_date": result.maturity_date.isoformat(),
            "notes": result.notes,
            "notes_summary": summarize_notes(result.notes),
        }
    )
