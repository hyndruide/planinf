# app/pattern_engine/views.py
from rest_framework import viewsets
from .models import TrameModel
from .serializers import TrameSerializer

class TrameViewSet(viewsets.ModelViewSet):
    queryset = TrameModel.objects.all()
    serializer_class = TrameSerializer
