from django.shortcuts import render
# Create your views here
from django.db import models
from .models import CoalMine, EmissionRecord, CarbonSink, GapAnalysis
from .serializers import CoalMineSerializer, EmissionSerializer, CarbonSinkSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

class CoalMineCreateView(generics.ListCreateAPIView):
    queryset = CoalMine.objects.all()
    serializer_class = CoalMineSerializer


class EmissionViewSet(generics.ListCreateAPIView):
    queryset = EmissionRecord.objects.all()
    serializer_class = EmissionSerializer

class CarbonSinkListCreateView(generics.ListCreateAPIView):
    queryset = CarbonSink.objects.all()
    serializer_class = CarbonSinkSerializer

class GapAnalysisView(APIView):
    def post(self, request):
        totalEmissions = EmissionRecord.objects.aggregate(total=models.Sum('total_emissions_kg'))['total'] or 0
        carbonSinkCapacity = CarbonSink.objects.aggregate(total= models.Sum('afforestation_offset'))['total'] or 0

        gapValue = round(totalEmissions - carbonSinkCapacity, 2)

        shortfall_areas = []
        
        # Check key areas in emissions data
        latest_emission = EmissionRecord.objects.last()
        if latest_emission:
            if latest_emission.fuel_usage_liters > 1000:  # Example threshold
                shortfall_areas.append({
                    "area": "Fuel Usage",
                    "issue": "High fuel consumption detected.",
                    "suggestion": "Switch to fuel-efficient or electric machinery."
                })
            
            if latest_emission.transportation_cost > 500:  # Example threshold
                shortfall_areas.append({
                    "area": "Transportation",
                    "issue": "High transportation emissions.",
                    "suggestion": "Optimize transportation routes and adopt efficient logistics."
                })

            if latest_emission.electricity_usage_kwh > 2000:  # Example threshold
                shortfall_areas.append({
                    "area": "Electricity Usage",
                    "issue": "Excessive electricity usage detected.",
                    "suggestion": "Adopt renewable energy sources like solar and wind."
                })


        if gapValue <= 0 :
            recommendations = "Carbon neutrality achieved. Maintain current sustainability practices."
        else:
            recommendations = ' | '.join([
                "Expand afforestation efforts.",
                "Use cleaner fuel alternatives (electric vehicles, biodiesel).",
                "Optimize coal transportation routes.",
                "Invest in renewable energy sources (solar/wind).",
            ])

        gapAnalysis = GapAnalysis.objects.create(
            gap_value = gapValue,
            recommendations = recommendations
        )

        return Response ({
            'gap_value': gapValue,
            'recommendations': recommendations,
            'shortfall_areas': shortfall_areas
        }, status=status.HTTP_201_CREATED)
    

class dashboardView(APIView):
    def get(self, request):
        emissionsData = EmissionRecord.objects.values(
            'excavation_tonnes', 'transportation_cost', 'fuel_usage_liters', 'electricity_usage_kwh'
        ).last() or {}

        gapData = GapAnalysis.objects.last()
        carbonSinkData = CarbonSink.objects.aggregate(total=models.Sum('afforestation_offset'))['total'] or 0

        return Response ({
            'emission_breakdown': emissionsData,
            'carbon_sink_capacity': carbonSinkData,
            'gap_value': gapData.gap_value if gapData else 0,
        })




# def visualize_emissions(request):
#     emissions = Emission.objects.values('coal_mine', 'year', 'co2_emissions', 'methane_emissions')
#     mines = list(set(e['coal_mine'] for e in emissions))
#     years = sorted(set(e['year'] for e in emissions))

#     # Data preparation
#     co2_data = {mine: [] for mine in mines}
#     methane_data = {mine: [] for mine in mines}
#     for year in years:
#         for mine in mines:
#             emission = next((e for e in emissions if e['year'] == year and e['coal_mine'] == mine), None)
#             co2_data[mine].append(emission['co2_emissions'] if emission else 0)
#             methane_data[mine].append(emission['methane_emissions'] if emission else 0)


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

# class EmissionFactorsView(APIView):
#     def get(self, request):
#         # Call the service function to fetch emission factors
#         emission_factors = fetch_emission_factors()
#         if emission_factors:
#             return Response(emission_factors, status=200)
#         return Response({"error": "Unable to fetch emission factors"}, status=500)

# class CarbonCreditsView(APIView):
#     def get(self, request):
#         # Call the service function to fetch carbon credit rates
#         carbon_credits = fetch_carbon_credit_rates()
#         if carbon_credits:
#             return Response(carbon_credits, status=200)
#         return Response({"error": "Unable to fetch carbon credit rates"}, status=500)

# class AfforestationPlansView(APIView):
#     def get(self, request):
#         # Call the service function to fetch afforestation plans
#         afforestation_plans = fetch_afforestation_plans()
#         if afforestation_plans:
#             return Response(afforestation_plans, status=200)
#         return Response({"error": "Unable to fetch afforestation plans"}, status=500)
    

# from rest_framework.generics import ListAPIView
# from .models import EmissionFactor, CarbonCreditRate, AfforestationPlan
# from .serializers import EmissionFactorSerializer, CarbonCreditRateSerializer, AfforestationPlanSerializer

# View to handle API requests for EmissionFactor
# class EmissionFactorListView(generics.ListAPIView):
#     queryset = EmissionFactor.objects.all()  # Fetch all emission factors from the database
#     serializer_class = EmissionFactorSerializer  # Use the serializer to return JSON response

# # View to handle API requests for CarbonCreditRate
# class CarbonCreditRateListView(generics.ListAPIView):
#     queryset = CarbonCreditRate.objects.all()  # Fetch all carbon credit rates
#     serializer_class = CarbonCreditRateSerializer

# # View to handle API requests for AfforestationPlan
# class AfforestationPlanListView(generics.ListAPIView):
#     queryset = AfforestationPlan.objects.all()  # Fetch all afforestation plans
#     serializer_class = AfforestationPlanSerializer

# class EmissionEstimationView(APIView):
#     """
#     API View to calculate emissions based on user input.
#     """

#     def post(self, request):
#         # Extract user inputs from the request body
#         coal_production = request.data.get("coal_production")  # in tonnes
#         methane_emission_factor = request.data.get("methane_emission_factor")  # m³ CH₄/tonne
#         other_emission_factors = request.data.get("other_emission_factors")  # optional
        
#         # Validate inputs
#         if not coal_production or not methane_emission_factor:
#             return Response({"error": "Coal production and methane emission factor are required."},
#                             status=status.HTTP_400_BAD_REQUEST)

#         # Calculate emissions
#         emissions = calculate_emissions(coal_production, methane_emission_factor, other_emission_factors)

#         return Response({
#             "coal_production": coal_production,
#             "methane_emission_factor": methane_emission_factor,
#             "emissions": emissions
#         }, status=status.HTTP_200_OK)
    



# class EmissionEstimationView(APIView):
#     permission_classes = [IsAuthenticated]  # Require authentication for this view

#     def post(self, request):
#         coal_production = request.data.get("coal_production")  # in tonnes
#         methane_emission_factor = request.data.get("methane_emission_factor")  # m³ CH₄/tonne
#         other_emission_factors = request.data.get("other_emission_factors")

#         if not coal_production or not methane_emission_factor:
#             return Response({"error": "Coal production and methane emission factor are required."},
#                             status=status.HTTP_400_BAD_REQUEST)

#         emissions = calculate_emissions(coal_production, methane_emission_factor, other_emission_factors)

#         # Save result to database
#         EmissionResult.objects.create(
#             coal_production=coal_production,
#             methane_emission_factor=methane_emission_factor,
#             methane_emissions=emissions["methane_emissions"],
#             methane_emissions_co2e=emissions["methane_emissions_co2e"],
#             co2_emissions=emissions["co2_emissions"],
#             total_emissions=emissions["total_emissions"]
#         )

#         return Response({
#             "coal_production": coal_production,
#             "methane_emission_factor": methane_emission_factor,
#             "emissions": emissions
#         }, status=status.HTTP_200_OK)

    

# import matplotlib.pyplot as plt
# from django.http import HttpResponse
# from .models import EmissionResult

# class EmissionVisualizationView(APIView):
#     """
#     Generate a visualization of emissions stored in the database.
#     """

#     def get(self, request):
#         # Fetch emissions data
#         results = EmissionResult.objects.all()
#         years = range(1, len(results) + 1)  # For simplicity, use record order as year
#         methane_emissions = [result.methane_emissions for result in results]
#         co2_emissions = [result.co2_emissions for result in results]
#         total_emissions = [result.total_emissions for result in results]

#         # Plot the data
#         plt.figure(figsize=(10, 6))
#         plt.plot(years, methane_emissions, label="Methane Emissions (CH₄)", marker='o')
#         plt.plot(years, co2_emissions, label="CO₂ Emissions", marker='o')
#         plt.plot(years, total_emissions, label="Total Emissions", marker='o')
#         plt.xlabel("Year")
#         plt.ylabel("Emissions (tonnes)")
#         plt.title("Emissions Trends")
#         plt.legend()
#         plt.grid(True)
#         plt.tight_layout()

#         # Save the plot to a temporary file
#         plt.savefig('emissions_plot.png')
#         plt.close()

#         # Return the plot as an HTTP response
#         with open('emissions_plot.png', 'rb') as f:
#             return HttpResponse(f.read(), content_type="image/png")

