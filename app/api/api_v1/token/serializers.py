from rest_framework import serializers
from models_v1.models import Admin

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = [
            "id",
            "name",
            "email",
            "password",
            "is_mailauth_completed",
            "is_enabled",
            "config",
            "is_super",
        ]    
