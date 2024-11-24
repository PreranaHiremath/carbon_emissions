from .models import EmissionFactor

def calculate_emissions(coal_production, methane_emission_factor, other_emission_factors=None):
    """
    Calculate CO2 and Methane emissions based on user inputs and emission factors.

    :param coal_production: Annual coal production in tonnes
    :param methane_emission_factor: Emission factor for methane (m³ CH₄/tonne)
    :param other_emission_factors: Dictionary of other emission factors (e.g., fuel usage)
    :return: Dictionary with CO2 and Methane emissions
    """
    # Methane emissions (CH₄)
    methane_emissions = coal_production * methane_emission_factor  # m³ CH₄

    # Convert Methane emissions to CO2 equivalent
    methane_to_co2e_conversion = 25  # Global Warming Potential (GWP) factor for methane
    methane_emissions_co2e = methane_emissions * methane_to_co2e_conversion

    # Additional emissions (e.g., fuel, electricity)
    co2_emissions = 0
    if other_emission_factors:
        for activity, factor in other_emission_factors.items():
            co2_emissions += factor.get('value', 0) * factor.get('activity_data', 0)

    # Total emissions
    total_emissions = co2_emissions + methane_emissions_co2e

    return {
        "methane_emissions": methane_emissions,
        "methane_emissions_co2e": methane_emissions_co2e,
        "co2_emissions": co2_emissions,
        "total_emissions": total_emissions,
    }
