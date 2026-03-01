from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PolitiqueConformiteViewSet, PlanningAuditAPIView

router = DefaultRouter()
router.register(r'politiques', PolitiqueConformiteViewSet, basename='politiques')

urlpatterns = [
    path('audit/', PlanningAuditAPIView.as_view(), name='planning_audit'),
    path('', include(router.urls)),
]
