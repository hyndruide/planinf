# app/applied_planning/admin.py
from django.contrib import admin
from .models import AffectationModel, AbsenceModel

@admin.register(AffectationModel)
class AffectationAdmin(admin.ModelAdmin):
    list_display = ('agent', 'trame', 'date_debut')
    search_fields = ('agent__nom', 'trame__nom')
    list_filter = ('date_debut',)
    raw_id_fields = ('agent', 'trame')

@admin.register(AbsenceModel)
class AbsenceAdmin(admin.ModelAdmin):
    list_display = ('agent', 'type_absence', 'date_debut', 'date_fin')
    search_fields = ('agent__nom',)
    list_filter = ('type_absence', 'date_debut')
    raw_id_fields = ('agent',)
