"""
URL Configuration for planinf

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path  # Use 'path' instead of 'url'

urlpatterns = [
    path('admin/', admin.site.urls),
]