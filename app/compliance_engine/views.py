from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from .models import PolitiqueConformiteModel
from .serializers import PolitiqueConformiteSerializer
from .services import run_planning_audit

class PolitiqueConformiteViewSet(viewsets.ReadOnlyModelViewSet):
# ... (rest of the class)
    queryset = PolitiqueConformiteModel.objects.all()
    serializer_class = PolitiqueConformiteSerializer

class PlanningAuditAPIView(APIView):
    """
    API pour exécuter un audit de conformité sur un planning.
    """
    def get(self, request):
        agent_id = request.query_params.get('agent_id')
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        politique_ids = request.query_params.getlist('politique_ids') or request.query_params.getlist('politique_ids[]')

        if not agent_id or not start_date_str or not end_date_str:
            return Response(
                {"error": "agent_id, start_date and end_date are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            report = run_planning_audit(agent_id, start_date, end_date, politique_ids)
            return Response(report, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
