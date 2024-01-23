from rest_framework import serializers
from .models import DatabaseCredentials


class DatabaseCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseCredentials
        fields = '__all__'
