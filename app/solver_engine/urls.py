# app/solver_engine/urls.py
from django.urls import path
from .api_views import GenerateScheduleAPIView

urlpatterns = [
    path('generate/', GenerateScheduleAPIView.as_view(), name='generate_schedule'),
]
