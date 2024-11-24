import requests
from django.db import models
# Fetch Emission Factors from External API
def fetch_emission_factors():
    url = "https://example.com/emission-factors"  # Replace with actual API URL
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()  # Assuming API returns JSON data
    except requests.RequestException as e:
        print(f"Error fetching emission factors: {e}")
        return {}

# Fetch Carbon Credit Rates from External API
def fetch_carbon_credit_rates():
    url = "https://example.com/carbon-credits"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()  # Assuming API returns JSON data
    except requests.RequestException as e:
        print(f"Error fetching carbon credit rates: {e}")
        return {}

# Fetch Afforestation Plans from External API
def fetch_afforestation_plans():
    url = "https://example.com/afforestation-plans"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()  # Assuming API returns JSON data
    except requests.RequestException as e:
        print(f"Error fetching afforestation plans: {e}")
        return {}


def save_emission_factors():
    data = fetch_emission_factors()  # Assume this fetches API data
    for item in data:
        EmissionFactor.objects.update_or_create(
            gas_name=item.get("gas_name"),
            defaults={
                "factor": item.get("factor"),
                "unit": item.get("unit"),
            }
        )

def save_carbon_credit_rates():
    data = fetch_carbon_credit_rates()  # Assume this fetches API data
    for item in data:
        CarbonCreditRate.objects.update_or_create(
            region=item.get("region"),
            defaults={"credit_rate": item.get("credit_rate")},
        )

def save_afforestation_plans():
    data = fetch_afforestation_plans()  # Assume this fetches API data
    for item in data:
        AfforestationPlan.objects.update_or_create(
            region=item.get("region"),
            defaults={
                "description": item.get("description"),
                "estimated_carbon_offset": item.get("estimated_carbon_offset"),
            }
        )
