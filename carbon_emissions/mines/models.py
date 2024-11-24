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

class Emission(models.Model):
    coal_mine = models.ForeignKey(CoalMine, on_delete=models.CASCADE, related_name="emissions")
    year = models.IntegerField()
    co2_emissions = models.FloatField()  # in tonnes
    methane_emissions = models.FloatField()  # in tonnes CO2 equivalent

    def __str__(self):
        return f"Emission record for {self.coal_mine.name} in {self.year}"



class EmissionFactor(models.Model):
    gas_name = models.CharField(max_length=100)  # e.g., Methane, CO2
    factor = models.FloatField()  # Emission factor value
    unit = models.CharField(max_length=50)  # e.g., kg CO2 per tonne

    def __str__(self):
        return f"{self.gas_name} ({self.unit})"

class CarbonCreditRate(models.Model):
    region = models.CharField(max_length=100)  # e.g., India, USA
    credit_rate = models.FloatField()  # Carbon credit value per tonne

    def __str__(self):
        return f"{self.region}: {self.credit_rate}"

class AfforestationPlan(models.Model):
    region = models.CharField(max_length=100)
    description = models.TextField()
    estimated_carbon_offset = models.FloatField()  # e.g., tonnes of CO2 offset

    def __str__(self):
        return f"{self.region} Plan"


class EmissionResult(models.Model):
    coal_production = models.FloatField()
    methane_emission_factor = models.FloatField()
    methane_emissions = models.FloatField()
    methane_emissions_co2e = models.FloatField()
    co2_emissions = models.FloatField()
    total_emissions = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Emission Result on {self.timestamp}"












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
