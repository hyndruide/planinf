from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .services import calculate_agent_balance

class AgentBalanceAPIView(APIView):
    """
    API pour récupérer la balance horaire d'un agent.
    """
    def get(self, request, agent_id):
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
            return Response(
                {"error": "Invalid date format, use YYYY-MM-DD"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            result = calculate_agent_balance(agent_id, start_date, end_date)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
