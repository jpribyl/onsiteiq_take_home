from django.contrib.auth import models as django_contrib_auth_models
from rest_framework import serializers


class WebSafeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = django_contrib_auth_models.User
        fields = ["first_name", "last_name", "email"]
