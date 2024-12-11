from django.db import models

class CoalMine(models.Model):
    MINE_TYPES = [
        ('open_pit', 'Open Pit'),
        ('underground', 'Underground'),
    ]

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    mine_type = models.CharField(max_length=50, choices=MINE_TYPES)
    coal_production_tonnes = models.FloatField()  # Annual coal production in tonnes
    methane_emission_factor = models.FloatField()  # Methane emission factor (e.g., m³ CH₄/tonne of coal)

    def __str__(self):
        return self.name

class EmissionRecord(models.Model):
    excavation_tonnes = models.FloatField()
    transportation_cost = models.FloatField()  # e.g., per km or per tonne
    fuel_usage_liters = models.FloatField()  # Fuel for equipment
    electricity_usage_kwh = models.FloatField()  # Electricity for accommodation
    total_emissions_kg = models.FloatField(null=True, blank=True)

    def calculate_emissions(self):
        diesel_emission_factor = 2.68  # kg CO2e per liter
        electricity_emission_factor = 0.85  # kg CO2e per kWh
        transportation_emission_factor = 0.25  # kg CO2e per km/tonne
        
        emissions = (
            self.fuel_usage_liters * diesel_emission_factor +
            self.electricity_usage_kwh * electricity_emission_factor +
            self.transportation_cost * transportation_emission_factor
        )
        return round(emissions, 2)

    def save(self, *args, **kwargs):
        self.total_emissions_kg = self.calculate_emissions()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Emission Record - {self.id} ({self.total_emissions_kg} kg CO2e)"


class CarbonSink(models.Model):
    MINE_LOCATIONS = [
        ('jharkhand', 'Jharkhand'),
        ('rajasthan', 'Rajasthan'),
        ('assam', 'Assam'),
        ('other', 'Other'),
    ]

    mine_location = models.CharField(max_length=20, choices=MINE_LOCATIONS, default='other')
    forest_area_hectares = models.FloatField()
    sequestration_rate = models.FloatField(null=True, blank=True)  # kg CO2e per hectare/year
    total_sequestration = models.FloatField(null=True, blank=True)

    def calculate_sequestration_rate(self):
        # Example Factors (based on hypothetical data)
        location_factor = {
            'jharkhand': 12000,  # kg CO2e/hectare/year
            'rajasthan': 4000,   # Lower due to arid conditions
            'assam': 15000,      # High due to dense vegetation
            'other': 8000,       # Default fallback
        }
        return location_factor.get(self.mine_location, 8000)

    def save(self, *args, **kwargs):
        self.sequestration_rate = self.calculate_sequestration_rate()
        self.total_sequestration = self.forest_area_hectares * self.sequestration_rate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.mine_location.capitalize()} - Sequestration: {self.total_sequestration} kg CO2e"


class GapAnalysis (models.Model):
    gap_value = models.FloatField(null=True, blank=True)
    recommendations = models.TextField(null = True, blank=True)

    def __str__(self):
        return f"Gap: {self.gap_value} kg CO2e"


# class EmissionFactor(models.Model):
#     gas_name = models.CharField(max_length=100)  # e.g., Methane, CO2
#     factor = models.FloatField()  # Emission factor value
#     unit = models.CharField(max_length=50)  # e.g., kg CO2 per tonne

#     def __str__(self):
#         return f"{self.gas_name} ({self.unit})"

# class CarbonCreditRate(models.Model):
#     region = models.CharField(max_length=100)  # e.g., India, USA
#     credit_rate = models.FloatField()  # Carbon credit value per tonne

#     def __str__(self):
#         return f"{self.region}: {self.credit_rate}"

# class AfforestationPlan(models.Model):
#     region = models.CharField(max_length=100)
#     description = models.TextField()
#     estimated_carbon_offset = models.FloatField()  # e.g., tonnes of CO2 offset

#     def __str__(self):
#         return f"{self.region} Plan"


# class EmissionResult(models.Model):
#     coal_production = models.FloatField()
#     methane_emission_factor = models.FloatField()
#     methane_emissions = models.FloatField()
#     methane_emissions_co2e = models.FloatField()
#     co2_emissions = models.FloatField()
#     total_emissions = models.FloatField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Emission Result on {self.timestamp}"












# from mines.models import CoalMine

# Retrieve all records
# all_coal_mines = CoalMine.objects.all()

# Display each record's details
# for mine in all_coal_mines:
    # print(mine.id, mine.name, mine.location, mine.mine_type, mine.coal_production_tonnes, mine.methane_emission_factor)


# class Emission(models.Model):
#     coal_mine = models.ForeignKey(CoalMine, on_delete=models.CASCADE, related_name="emissions")
#     year = models.IntegerField()
#     co2_emissions = models.FloatField()  # Calculated CO₂ emissions in tonnes
#     ch4_emissions = models.FloatField()  # Calculated CH₄ emissions in tonnes

#     @property
#     def carbon_dioxide_equivalent(self):
#         return self.co2_emissions + (self.ch4_emissions * 25)  # Convert CH₄ to CO₂e

#     def __str__(self):
#         return f"{self.coal_mine.name} - {self.year}"
