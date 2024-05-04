from django.urls import path
from . views import *

urlpatterns = [
    #Chapa checkout
    path("chapa_checkout/", chapa_checkout, name="chapa_checkout"),

    # PayPal chekout
    path("paypal_checkout/",paypal_checkout, name="paypal_checkout"),

    # Stripe Checkout
    path("stripe_checkout/",stripe_checkout_sheet, name="stripe_checkout"),

]