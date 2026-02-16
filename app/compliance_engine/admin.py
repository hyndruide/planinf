# app/compliance_engine/admin.py
from django.contrib import admin
from .models import PolitiqueConformiteModel

@admin.register(PolitiqueConformiteModel)
class PolitiqueConformiteAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
