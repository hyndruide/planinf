# app/pattern_engine/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrameViewSet

router = DefaultRouter()
router.register(r'trames', TrameViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
