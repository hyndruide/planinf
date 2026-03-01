from django.urls import path
from .views import AgentBalanceAPIView

urlpatterns = [
    path('balance/<uuid:agent_id>/', AgentBalanceAPIView.as_view(), name='agent_balance'),
]
