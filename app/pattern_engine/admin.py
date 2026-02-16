# app/pattern_engine/admin.py
from django.contrib import admin
from .models import TrameModel

@admin.register(TrameModel)
class TrameAdmin(admin.ModelAdmin):
    list_display = ('nom', 'duree_cycle_jours')
    search_fields = ('nom',)
    list_filter = ('duree_cycle_jours',)
