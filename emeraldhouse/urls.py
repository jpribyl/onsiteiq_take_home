from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from rest_framework_simplejwt import views as rest_framework_views

from emeraldhouse.api import applicant_api

router = routers.DefaultRouter()
router.register(r"applicants", applicant_api.ApplicantViewSet)
router.register(r"applicant_notes", applicant_api.ApplicantNoteViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # simplejwt views according to docs:
    # https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html
    path(
        "api/token/",
        rest_framework_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        rest_framework_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/token/verify/",
        rest_framework_views.TokenVerifyView.as_view(),
        name="token_verify",
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(), name="swagger-ui"),
]
