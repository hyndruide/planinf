# app/applied_planning/serializers.py
from rest_framework import serializers
from .models import AffectationModel, AbsenceModel

class AffectationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffectationModel
        fields = '__all__'

class AbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceModel
        fields = '__all__'
