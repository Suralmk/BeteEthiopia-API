from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from . models import PaymentHistory
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY
from . serializers import *
class BookingPayment(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        customer = stripe.Customer.create()
        ephemeralKey = stripe.EphemeralKey.create(
            customer=customer['id'],
            stripe_version='2024-04-10',
            )
        paymentIntent = stripe.PaymentIntent.create(
            amount=1099,
            currency='eur',
            customer=customer['id'],
                automatic_payment_methods={
                'enabled': True,
                },
        )

        return Response({
            "paymentIntent":paymentIntent.client_secret,
            "ephemeralKey":ephemeralKey.secret,
            "customer":customer.id,
        })


class PaymentIntent(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        amount = request.data.get('amount', 0)
        booking_id = request.data.get('booking_id')
        try:
            customer = stripe.Customer.create()
            paymentIntent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                customer=customer['id'],
                    automatic_payment_methods={
                    'enabled': True,
                    },
                metadata={'booking_id': booking_id, 'user_id': request.user.id},
            )
            return Response({
                "paymentIntent":paymentIntent.client_secret,
                 "customer":customer.id,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
             return Response({
                "message":e,
            }, status=status.HTTP_400_BAD_REQUEST)

class PaymentHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        history = PaymentHistory.objects.filter(user=request.user).all()
        if history is not None:
            serializer = PaymentHistorySerializer(history, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message" : "Payment hostory not found"}, status=status.HTTP_404_NOT_FOUND)
        
        