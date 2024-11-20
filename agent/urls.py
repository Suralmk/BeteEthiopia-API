from django.urls import path
from . views import *

urlpatterns = [
    path("agents/", TourAgentView.as_view(), name="agent_list"),
    path("agents/<int:id>/", TourAgentDetailView.as_view(), name="agent_detail"),
    path("agents/<int:id>/destination/", TourAgentDestinationsView.as_view(), name="agent_destination"),
]