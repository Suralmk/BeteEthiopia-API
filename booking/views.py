from django.shortcuts import render, get_object_or_404
from rest_framework import permissions,  status, generics
from rest_framework.response import Response
from . serializers import *
from rest_framework.views import APIView
from . models import Booking
from destination.models import Destination
from agent.models import Agent

class BookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, booking_id = None):
        
        if booking_id is not None:
            booking = get_object_or_404(Booking, id=booking_id)
        
        serilaized_data = BookingSerializer(booking).data
        return Response(serilaized_data, status=status.HTTP_200_OK)
    
    def post(self, request):

        data =  request.data

        data["user"] = request.user.id
        data["phone_no"] = int(data["phone_no"])
        data["guest_number"] = int(data["guest_number"])
        print(data)
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

