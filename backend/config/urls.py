"""URL configuration for the onion DSS backend."""
from __future__ import annotations

from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("dss.urls")),
]


def healthcheck(_request):
    """Simple health endpoint that can be used by front-end deployments."""
    return JsonResponse({"status": "ok"})


urlpatterns.append(path("healthz", healthcheck))
