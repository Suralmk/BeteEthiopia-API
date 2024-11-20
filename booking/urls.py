from django.urls import path
from . views import *

urlpatterns = [
    path("", BookingView.as_view(), name="booking"),
    path("<int:id>/", BookingView.as_view(), name="booking_detail")
]