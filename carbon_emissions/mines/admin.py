from django.contrib import admin
from .models import EmissionFactor, CarbonCreditRate, AfforestationPlan

@admin.register(EmissionFactor)
class EmissionFactorAdmin(admin.ModelAdmin):
    list_display = ("gas_name", "factor", "unit")

@admin.register(CarbonCreditRate)
class CarbonCreditRateAdmin(admin.ModelAdmin):
    list_display = ("region", "credit_rate")

@admin.register(AfforestationPlan)
class AfforestationPlanAdmin(admin.ModelAdmin):
    list_display = ("region", "estimated_carbon_offset")

class EmissionResultAdmin(admin.ModelAdmin):
    list_display = ("coal_production", "total_emissions", "timestamp")
