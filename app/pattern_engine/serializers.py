# app/pattern_engine/serializers.py
from rest_framework import serializers
from .models import TrameModel

class TrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrameModel
        fields = '__all__'
