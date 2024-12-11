from django.urls import path
from .views import EmissionViewSet, CoalMineCreateView, CarbonSinkListCreateView, GapAnalysisView, dashboardView


urlpatterns = [
    path('mine/', CoalMineCreateView.as_view(), name='CoalMine'),
    path('emissions/', EmissionViewSet.as_view(), name='Emissions'),
    path('carbonSink/', CarbonSinkListCreateView.as_view(), name='CarbonSink'),
    path('gapAnalysis/', GapAnalysisView.as_view(), name = 'gapAnalysis'),
    path('dashboard/', dashboardView.as_view(), name = 'Dashboard'),
]
