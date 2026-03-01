# app/applied_planning/views.py
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from resource_management.models import AgentModel
from .models import AffectationModel, AbsenceModel
from .serializers import AffectationSerializer, AbsenceSerializer
from .services import get_agent_planning
from .reporting import calculate_service_fte

class AffectationViewSet(viewsets.ModelViewSet):
# ... (rest of file)
    queryset = AffectationModel.objects.all()
    serializer_class = AffectationSerializer

class AbsenceViewSet(viewsets.ModelViewSet):
    queryset = AbsenceModel.objects.all()
    serializer_class = AbsenceSerializer

class FullViewAPIView(APIView):
    def get(self, request):
        start_date_str = request.query_params.get('start_date')
        weeks_str = request.query_params.get('weeks', '12')
        
        if not start_date_str:
            return Response({"error": "start_date is required"}, status=400)
            
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            weeks = int(weeks_str)
        except ValueError:
            return Response({"error": "Invalid format for start_date or weeks"}, status=400)
            
        end_date = start_date + timedelta(weeks=weeks) - timedelta(days=1)
        
        agents = AgentModel.objects.all()
        result = []
        for agent in agents:
            planning = get_agent_planning(agent.id, start_date, end_date)
            
            planning_data = []
            for day in planning:
                planning_data.append({
                    'date': day.date,
                    'shift': {
                        'type': day.shift.type.value if hasattr(day.shift.type, 'value') else str(day.shift.type),
                        'duration': day.shift.duration
                    }
                })
            
            result.append({
                'agent_id': agent.id,
                'nom': agent.nom,
                'planning': planning_data
            })
            
        return Response(result)

class FTEReportAPIView(APIView):
    """
    API pour récupérer le rapport ETP (Équivalent Temps Plein) du service.
    """
    def get(self, request):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        
        if not start_date_str or not end_date_str:
            return Response(
                {"error": "start_date and end_date are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            report = calculate_service_fte(start_date, end_date)
            return Response(report, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
