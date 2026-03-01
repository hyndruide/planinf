from rest_framework import viewsets
from .models import PolitiqueConformiteModel
from .serializers import PolitiqueConformiteSerializer

class PolitiqueConformiteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows policies to be viewed.
    Read-only since policies are managed via the admin interface for now.
    """
    queryset = PolitiqueConformiteModel.objects.all()
    serializer_class = PolitiqueConformiteSerializer
