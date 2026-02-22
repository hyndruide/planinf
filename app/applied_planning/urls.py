# app/applied_planning/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FullViewAPIView, AffectationViewSet, AbsenceViewSet

router = DefaultRouter()
router.register(r'affectations', AffectationViewSet)
router.register(r'absences', AbsenceViewSet)

urlpatterns = [
    path('full-view/', FullViewAPIView.as_view(), name='full_view'),
    path('', include(router.urls)),
]
