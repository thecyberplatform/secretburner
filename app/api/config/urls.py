from django.urls import re_path, include

api_urlpatterns = [
    re_path(r"^secret/", include(("secret.api.secret", "secret"), namespace="secret")),
    re_path(
        r"^request/", include(("secret.api.request", "request"), namespace="request")
    ),
    re_path(r"^verify/", include(("secret.api.verify", "verify"), namespace="verify")),
]

urlpatterns = [
    re_path(r"^api/", include((api_urlpatterns, "api"), namespace="api")),
]
