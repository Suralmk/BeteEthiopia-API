import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from api.models import User
from booking.models import Booking
from django.shortcuts import get_object_or_404
from  . models import PaymentHistory
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
@api_view(['POST'])
def stripe_webhook(request):
    payload = request.data

    try:
         event = stripe.Event.construct_from(
      payload, stripe.api_key
    )
    except ValueError as e:
        print(f"Invalid payload: {e}")
        return JsonResponse(status=400, data={"error" : "Error Upgrading to premium"})
    except stripe.error.SignatureVerificationError as e:
        print(f"Invalid signature: {e}")
        return JsonResponse(status=400, data={"error" : "Error Upgrading to premium"})

    if event['type'] == 'payment_intent.succeeded':
        data = event['data']['object'] 
        upgraded = handle_booking_session(data)

        if not upgraded:
            return JsonResponse(status=400, data={"error" : "Error Upgrading to premium"})
        return JsonResponse(status=200, data={"error" : "Payment succesful"})
    return JsonResponse(status=200, data=payload)
            
def handle_booking_session(data):
    booking_id = data['metadata']['booking_id']
    user_id = data['metadata']['user_id']
    amount = data["amount"]
    booking =get_object_or_404(Booking, id=booking_id)
    user =get_object_or_404(User, id=user_id)
    if booking:
        if user:
           history =  PaymentHistory.objects.create(
               amount=amount,
               user=user, booking=booking
           )
           history.save()
        else:
            return False
        
        booking.paid = True
        booking.save()
        return True
    else:
        return False