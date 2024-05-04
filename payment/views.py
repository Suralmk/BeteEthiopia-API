from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.decorators import api_view
from api . utils import get_transaction_number
from api.models import Destination

import chapa
chapaAPP = chapa.Chapa("sk_test_4eC39HqLyjWDarjtT1zdp7dc")

import paypal

import stripe
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'


@api_view(["POST"])
def chapa_checkout(request, destination_id=None): 

    if destination_id is None:
        destination_obj_id = request.data.get('destination_id', None)
    else:
        destination_obj_id= destination_id
        
    order = Destination.objects.get( id=destination_obj_id)
    
    if request.method == "POST":

        transaction_id = get_transaction_number(destination_id)
        success_url = ""
        data = {
                "email":order.email,
                "amount" :order.get_total_cost(),
                "first_name":order.first_name,
                "last_name":order.last_name,
                "tx_ref":transaction_id,
                "callback_url":"https://127.0.0.1:1200/",
                "return_url":success_url,
                "customization":{
                    "title" : "Woozie Checkout",
                    "description" :"You are paying to checkout a product from woozie"
                }
            }
        
        response = chapaAPP.initialize(**data)
        chapaAPP.verify(transaction_id)

    return Response({
        "checkout_url" : response["data"].get("checkout_url")
    })

def paypal_checkout(request):
    pass

@login_required()
def stripe_checkout_sheet(request):
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