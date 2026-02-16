# app/applied_planning/admin.py
from django.contrib import admin
from .models import AffectationModel

@admin.register(AffectationModel)
class AffectationAdmin(admin.ModelAdmin):
    list_display = ('agent', 'trame', 'date_debut')
    search_fields = ('agent__nom', 'trame__nom')
    list_filter = ('date_debut',)
    raw_id_fields = ('agent', 'trame') # Pour faciliter la sélection dans l'admin si beaucoup d'agents/trames
