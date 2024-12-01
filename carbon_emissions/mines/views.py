from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets
from .models import CoalMine, Emission
from .serializers import CoalMineSerializer, EmissionSerializer
import matplotlib.pyplot as plt
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import fetch_emission_factors, fetch_carbon_credit_rates, fetch_afforestation_plans
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import calculate_emissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import EmissionFactor, CarbonCreditRate, AfforestationPlan
from .serializers import EmissionFactorSerializer, CarbonCreditRateSerializer, AfforestationPlanSerializer

class CoalMineViewSet(viewsets.ModelViewSet):
    queryset = CoalMine.objects.all()
    serializer_class = CoalMineSerializer

class EmissionViewSet(viewsets.ModelViewSet):
    queryset = Emission.objects.all()
    serializer_class = EmissionSerializer


def visualize_emissions(request):
    emissions = Emission.objects.values('coal_mine__name', 'year', 'co2_emissions', 'methane_emissions')
    mines = list(set(e['coal_mine__name'] for e in emissions))
    years = sorted(set(e['year'] for e in emissions))

    # Data preparation
    co2_data = {mine: [] for mine in mines}
    methane_data = {mine: [] for mine in mines}
    for year in years:
        for mine in mines:
            emission = next((e for e in emissions if e['year'] == year and e['coal_mine__name'] == mine), None)
            co2_data[mine].append(emission['co2_emissions'] if emission else 0)
            methane_data[mine].append(emission['methane_emissions'] if emission else 0)

#     # Plot
#     plt.figure(figsize=(12, 6))
#     bar_width = 0.4
#     x = range(len(years))
#     for i, mine in enumerate(mines):
#         plt.bar([pos + (i * bar_width) for pos in x], co2_data[mine], bar_width, label=f"{mine} CO2")
#         plt.bar([pos + (i * bar_width) for pos in x], methane_data[mine], bar_width, bottom=co2_data[mine], label=f"{mine} Methane")

#     plt.xticks([pos + bar_width for pos in x], years)
#     plt.xlabel("Year")
#     plt.ylabel("Emissions (tonnes)")
#     plt.legend()
#     plt.title("Emissions per Coal Mine")
#     plt.savefig('grouped_emissions_plot.png')
#     with open('grouped_emissions_plot.png', 'rb') as f:
#         return HttpResponse(f.read(), content_type="image/png")

class EmissionFactorsView(APIView):
    def get(self, request):
        # Call the service function to fetch emission factors
        emission_factors = fetch_emission_factors()
        if emission_factors:
            return Response(emission_factors, status=200)
        return Response({"error": "Unable to fetch emission factors"}, status=500)

class CarbonCreditsView(APIView):
    def get(self, request):
        # Call the service function to fetch carbon credit rates
        carbon_credits = fetch_carbon_credit_rates()
        if carbon_credits:
            return Response(carbon_credits, status=200)
        return Response({"error": "Unable to fetch carbon credit rates"}, status=500)

class AfforestationPlansView(APIView):
    def get(self, request):
        # Call the service function to fetch afforestation plans
        afforestation_plans = fetch_afforestation_plans()
        if afforestation_plans:
            return Response(afforestation_plans, status=200)
        return Response({"error": "Unable to fetch afforestation plans"}, status=500)
    

# from rest_framework.generics import ListAPIView
# from .models import EmissionFactor, CarbonCreditRate, AfforestationPlan
# from .serializers import EmissionFactorSerializer, CarbonCreditRateSerializer, AfforestationPlanSerializer

# View to handle API requests for EmissionFactor
class EmissionFactorListView(ListAPIView):
    queryset = EmissionFactor.objects.all()  # Fetch all emission factors from the database
    serializer_class = EmissionFactorSerializer  # Use the serializer to return JSON response

# View to handle API requests for CarbonCreditRate
class CarbonCreditRateListView(ListAPIView):
    queryset = CarbonCreditRate.objects.all()  # Fetch all carbon credit rates
    serializer_class = CarbonCreditRateSerializer

# View to handle API requests for AfforestationPlan
class AfforestationPlanListView(ListAPIView):
    queryset = AfforestationPlan.objects.all()  # Fetch all afforestation plans
    serializer_class = AfforestationPlanSerializer

class EmissionEstimationView(APIView):
    """
    API View to calculate emissions based on user input.
    """

    def post(self, request):
        # Extract user inputs from the request body
        coal_production = request.data.get("coal_production")  # in tonnes
        methane_emission_factor = request.data.get("methane_emission_factor")  # m³ CH₄/tonne
        other_emission_factors = request.data.get("other_emission_factors")  # optional
        
        # Validate inputs
        if not coal_production or not methane_emission_factor:
            return Response({"error": "Coal production and methane emission factor are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Calculate emissions
        emissions = calculate_emissions(coal_production, methane_emission_factor, other_emission_factors)

        return Response({
            "coal_production": coal_production,
            "methane_emission_factor": methane_emission_factor,
            "emissions": emissions
        }, status=status.HTTP_200_OK)
    



class EmissionEstimationView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication for this view

    def post(self, request):
        coal_production = request.data.get("coal_production")  # in tonnes
        methane_emission_factor = request.data.get("methane_emission_factor")  # m³ CH₄/tonne
        other_emission_factors = request.data.get("other_emission_factors")

        if not coal_production or not methane_emission_factor:
            return Response({"error": "Coal production and methane emission factor are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        emissions = calculate_emissions(coal_production, methane_emission_factor, other_emission_factors)

        # Save result to database
        EmissionResult.objects.create(
            coal_production=coal_production,
            methane_emission_factor=methane_emission_factor,
            methane_emissions=emissions["methane_emissions"],
            methane_emissions_co2e=emissions["methane_emissions_co2e"],
            co2_emissions=emissions["co2_emissions"],
            total_emissions=emissions["total_emissions"]
        )

        return Response({
            "coal_production": coal_production,
            "methane_emission_factor": methane_emission_factor,
            "emissions": emissions
        }, status=status.HTTP_200_OK)

    

import matplotlib.pyplot as plt
from django.http import HttpResponse
from .models import EmissionResult

class EmissionVisualizationView(APIView):
    """
    Generate a visualization of emissions stored in the database.
    """

    def get(self, request):
        # Fetch emissions data
        results = EmissionResult.objects.all()
        years = range(1, len(results) + 1)  # For simplicity, use record order as year
        methane_emissions = [result.methane_emissions for result in results]
        co2_emissions = [result.co2_emissions for result in results]
        total_emissions = [result.total_emissions for result in results]

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(years, methane_emissions, label="Methane Emissions (CH₄)", marker='o')
        plt.plot(years, co2_emissions, label="CO₂ Emissions", marker='o')
        plt.plot(years, total_emissions, label="Total Emissions", marker='o')
        plt.xlabel("Year")
        plt.ylabel("Emissions (tonnes)")
        plt.title("Emissions Trends")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save the plot to a temporary file
        plt.savefig('emissions_plot.png')
        plt.close()

        # Return the plot as an HTTP response
        with open('emissions_plot.png', 'rb') as f:
            return HttpResponse(f.read(), content_type="image/png")
