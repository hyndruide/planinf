from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PolitiqueConformiteViewSet

router = DefaultRouter()
router.register(r'politiques', PolitiqueConformiteViewSet, basename='politiques')

urlpatterns = [
    path('', include(router.urls)),
]
