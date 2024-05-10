from django.urls import path, include
from . views import *
urlpatterns = [
    path("", home, name="home"),
    path("login/",LogInView.as_view(), name="login"),
    path("signup/",SignUpView.as_view(), name="signup"),

    # Tour agent
    path("agents/", TourAgentView.as_view(), name="agent_list"),
    path("agents/<int:id>/", TourAgentDetailView.as_view(), name="agent_detail"),
    path("agents/<int:id>/destination/", TourAgentDestinationsView.as_view(), name="agent_destination"),

    # Tour agent
    path("destination/", DestinationView.as_view(), name="destination_list"),
    path("destination/<int:id>/", DestinationDetailView.as_view(), name="destination_detail"),

    # Passwrod Reset
    path("get_otp/", get_otp, name="get_otp"),
    path("verify_otp/", verify_otp, name="verify_otp"),
    path("create_new_password/", CreateNewPassword.as_view(), name="create_new_password"),

    # Search
    path("search/<str:query>/", SearchView.as_view(), name="search"),

    # Search
    path("booking/", BookingView.as_view(), name="booking"),
    path("booking/<int:id>/", BookingDetailView.as_view(), name="booking_detail"),

    # Payment
    path('payment/', include("payment.urls")),
]
