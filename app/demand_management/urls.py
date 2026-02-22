# app/demand_management/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CoverageAnalysisAPIView, DailyRequirementViewSet

router = DefaultRouter()
router.register(r'requirements', DailyRequirementViewSet)

urlpatterns = [
    path('analysis/', CoverageAnalysisAPIView.as_view(), name='coverage_analysis'),
    path('', include(router.urls)),
]
