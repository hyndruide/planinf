# app/demand_management/views.py
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from .models import DailyRequirementModel
from .serializers import DailyRequirementSerializer
from .services import get_coverage_analysis

class DailyRequirementViewSet(viewsets.ModelViewSet):
    queryset = DailyRequirementModel.objects.all()
    serializer_class = DailyRequirementSerializer

class CoverageAnalysisAPIView(APIView):
    def get(self, request):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        
        if not start_date_str or not end_date_str:
            return Response({"error": "start_date and end_date are required"}, status=400)
            
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format, use YYYY-MM-DD"}, status=400)
            
        coverage = get_coverage_analysis(start_date, end_date)
        
        result = []
        for day in coverage:
            result.append({
                'date': day.date,
                'present_count': day.present_count,
                'required_count': day.required_count,
                'gap': day.gap
            })
            
        return Response(result)
