# app/demand_management/serializers.py
from rest_framework import serializers
from .models import DailyRequirementModel

class DailyRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyRequirementModel
        fields = '__all__'
