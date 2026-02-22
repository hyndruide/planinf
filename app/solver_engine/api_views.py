# app/solver_engine/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .services import generate_and_save_schedule

class GenerateScheduleAPIView(APIView):
    def post(self, request):
        agent_ids = request.data.get('agent_ids')
        politique_id = request.data.get('politique_id')
        duree_cycle = int(request.data.get('duree_cycle', 84))
        date_debut_str = request.data.get('date_debut')
        
        if not agent_ids or not politique_id or not date_debut_str:
            return Response(
                {"error": "agent_ids, politique_id and date_debut are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            date_debut = datetime.strptime(date_debut_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
            
        success = generate_and_save_schedule(agent_ids, politique_id, duree_cycle, date_debut)
        
        if success:
            return Response({"message": "Schedule generated successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "No feasible solution found"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
