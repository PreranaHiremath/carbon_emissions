from rest_framework import serializers
from .models import CoalMine, EmissionRecord,CarbonSink

class CoalMineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoalMine
        fields = '__all__'

class EmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionRecord
        fields = '__all__'

class CarbonSinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarbonSink
        fields = '__all__'


# class EmissionFactorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EmissionFactor
#         fields = "__all__"

# class CarbonCreditRateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CarbonCreditRate
#         fields = "__all__"

# class AfforestationPlanSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AfforestationPlan
#         fields = "__all__"

# # from rest_framework import serializers
# # from .models import EmissionFactor, CarbonCreditRate, AfforestationPlan

# class EmissionFactorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EmissionFactor
#         fields = "__all__"  # Include all fields in the API response

# class CarbonCreditRateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CarbonCreditRate
#         fields = "__all__"

# class AfforestationPlanSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AfforestationPlan
#         fields = "__all__"
