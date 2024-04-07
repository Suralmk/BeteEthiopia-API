from django.urls import path
from . views import *
urlpatterns = [
    path("", home, name="home"),
    path("login/",LogInView.as_view(), name="login"),
    path("signup/",SignUpView.as_view(), name="signup"),

    # Tour agent
    path("agents/", TourAgentView.as_view(), name="agent_list"),
    path("agents/<int:id>/", TourAgentDetailView.as_view(), name="agent_detail"),

    # Tour agent
    path("destination/", DestinationView.as_view(), name="destination_list"),
    path("destination/<int:id>/", DestinationDetailView.as_view(), name="destination_detail"),
]
