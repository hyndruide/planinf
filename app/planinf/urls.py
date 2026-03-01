"""
URL Configuration for planinf

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/resources/', include('resource_management.urls')),
    path('api/v1/patterns/', include('pattern_engine.urls')),
    path('api/v1/planning/', include('applied_planning.urls')),
    path('api/v1/coverage/', include('demand_management.urls')),
    path('api/v1/compliance/', include('compliance_engine.urls')),
    path('api/v1/solver/', include('solver_engine.urls')),
]