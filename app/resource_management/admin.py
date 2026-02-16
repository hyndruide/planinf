# app/resource_management/admin.py
from django.contrib import admin
from .models import AgentModel

@admin.register(AgentModel)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'quotite', 'date_debut_cycle')
    search_fields = ('nom',)
    list_filter = ('quotite',)
