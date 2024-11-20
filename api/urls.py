from django.urls import path, include
from . views import *
urlpatterns = [
    path("", home, name="home"),
    path("login/",LogInView.as_view(), name="login"),
    path("signup/",SignUpView.as_view(), name="signup"),

    # Password Reset
    path("get_otp/", get_otp, name="get_otp"),
    path("verify_otp/", verify_otp, name="verify_otp"),
    path("create_new_password/", CreateNewPassword.as_view(), name="create_new_password"),
    path("search/<str:query>/", SearchView.as_view(), name="search"),

    path("account/profile/", AccountView.as_view(), name="account"),
    path("account/payment-history/",  PaymentHistoryView.as_view(),  name="payment-history"),
    path("account/bookings/", BookingHistoryView.as_view(), name="account-booking"),

    path('payment/', include("payment.urls")),
    path('agent/', include("agent.urls")),
    path('destination/', include("destination.urls")),
    path('booking/', include("booking.urls")),
]
