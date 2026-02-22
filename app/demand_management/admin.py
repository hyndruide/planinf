# app/demand_management/admin.py
from django.contrib import admin
from .models import DailyRequirementModel

@admin.register(DailyRequirementModel)
class DailyRequirementAdmin(admin.ModelAdmin):
    list_display = ('get_day_of_week_display', 'required_count')
    ordering = ('day_of_week',)
