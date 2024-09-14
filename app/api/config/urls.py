from django.urls import re_path, include
from django.http import HttpResponse


def health_check(request):
    return HttpResponse(status=200)


api_urlpatterns = [
    re_path(r"^secret/", include(("secret.api.secret", "secret"), namespace="secret")),
    re_path(
        r"^request/", include(("secret.api.request", "request"), namespace="request")
    ),
    re_path(r"^verify/", include(("secret.api.verify", "verify"), namespace="verify")),
    re_path(r"^health-check/", health_check, name="health_check"),
]

urlpatterns = [
    re_path(r"^api/", include((api_urlpatterns, "api"), namespace="api")),
]
