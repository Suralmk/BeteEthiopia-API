from django.urls import path
from . views import *
from . webhook import stripe_webhook

urlpatterns = [
    path("intent/",PaymentIntent.as_view(), name="payment_intent"),
    path("history/",PaymentHistoryView.as_view(), name="payment_history"),
    path("webhook/",stripe_webhook, name="wehook"),
]