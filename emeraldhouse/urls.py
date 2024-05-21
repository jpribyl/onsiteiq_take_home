from django.urls import include, path
from rest_framework import routers
from emeraldhouse.api import applicant_api

router = routers.DefaultRouter()
router.register(r"applicants", applicant_api.ApplicantViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
