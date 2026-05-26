from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.db import connection


def healthz(request):
    """§3.7: /healthz endpoint — checks Postgres connectivity, returns 200/503."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ok"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "detail": str(e)}, status=503)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthz', healthz),
]
