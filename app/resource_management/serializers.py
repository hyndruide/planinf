# app/resource_management/serializers.py
from rest_framework import serializers
from .models import AgentModel

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentModel
        fields = '__all__'
