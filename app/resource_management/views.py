# app/resource_management/views.py
from rest_framework import viewsets
from .models import AgentModel
from .serializers import AgentSerializer

class AgentViewSet(viewsets.ModelViewSet):
    queryset = AgentModel.objects.all()
    serializer_class = AgentSerializer
