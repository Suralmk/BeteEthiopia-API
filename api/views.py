from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import permissions,  status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from . serializers import *

from . models import User       
from . utils import send_otp
from datetime import datetime
import pyotp
from destination.models import Destination
from django.contrib.auth import update_session_auth_hash
import base64
from django.core.files.base import ContentFile


@api_view(["GET"])
def home(request):
    return Response({"message" : "This is Zion Travel API" } ,status=200)

def get_auth_for_user(user, request):
   refresh =  RefreshToken.for_user(user)

   return {
       "user": UserSerializer(user, context={"request" : request}).data,
        "tokens" : {
            "refresh" : str(refresh),
            "access" : str(refresh.access_token)
        }
   }

class LogInView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(email=email, password=password)
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user_data = get_auth_for_user(user, request)

        return Response(user_data)

class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if User.objects.filter(email=email).exists():
            return Response({'message': 'Email already exists!'}, status=status.HTTP_400_BAD_REQUEST)

        new_user = SignUpSerializer(data=request.data)
        new_user.is_valid(raise_exception=True)
        user = new_user.save()
        user_data = get_auth_for_user(user, request)
        print(user_data)

        return Response(user_data ,status=status.HTTP_201_CREATED) 
    
@api_view(["POST"])
def get_otp(request):
    email = request.data.get("email")
    user = get_object_or_404(User, email=email)

    if user is None:
        return Response({"message": "Email does not exist"})
    
    data = {
            "message": "Otp succesfully send"
    }
    email_sent = send_otp(request, email)
    request.session["email"] = email

    if email_sent:
        data["email_sent"] = True

    return Response(data, status=status.HTTP_200_OK)
    
@api_view(["POST"])
def verify_otp(request):
    otp = request.data.get("otp")

    otp_secret = request.session["otp_secret"]
    otp_valid_time = request.session["otp_valid"]

    if otp_secret and otp_valid_time is not None:
        valid_until = datetime.fromisoformat(otp_valid_time)

        if valid_until > datetime.now():
            totp = pyotp.TOTP(otp_secret, interval=60)
            if totp.verify(otp):
                data = {
                            "message": "Otp succesfully Verified",
                            "verified":True
                        }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'OTP is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Otp has expired!'}, status=status.HTTP_400_BAD_REQUEST)
    else:
            return Response({'message': 'Otp is Required!'}, status=status.HTTP_400_BAD_REQUEST)

class CreateNewPassword(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        password = request.data.get("password")
        email =  request.session["email"]
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return Response({"message" : "Password Succesfully changed"},status=status.HTTP_201_CREATED )

#Search Agenst and Destination
class SearchView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, query=None):

        if query is not None:
            destination = Destination.objects.filter(
                Q(name__icontains=query) 
            ).all()
            
        if destination is not None:
            destination_data = SerachDestinationSerializer(
                destination, 
                many=True,
                context = {
                    "request": request
                }).data

        result = [a for a in destination_data  if a is not None ]

        return Response(
            result,
            status=status.HTTP_200_OK
        )
    
# Personal information views
class AccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user

        profile_data = {
            key : value for key, value in request.data.items() if key in ["first_name", "last_name", "email"]
        }
        password_data = {
            key : value for key, value in request.data.items() if key in ["old_password", "new_password"]
        }

        profile_image_data = {
            key: value for key, value in request.data.items() if key in ["profile_image"]
        }
        if profile_data:
            profile_serializer = ProfileUpdateSerializer(user, data=profile_data, partial=True)
            if profile_serializer.is_valid():
                profile_serializer.save()
            else:
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        if password_data:
            password_serializer = PasswordUpdateSerializer(user, data=password_data, partial=True)
            if password_serializer.is_valid(raise_exception=True):
                old_password = password_serializer.validated_data['old_password']
                new_password = password_serializer.validated_data['new_password']
                if not user.check_password(old_password):
                    return Response({"message"  : "Old password is incorrect!"},  status=status.HTTP_400_BAD_REQUEST)

                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
            else:
                return Response(password_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        if profile_image_data: 
            photo = request.data.get("profile_image")
            try:
            
                if ";base64," in photo:
                    format, imgstr = photo.split(";base64,")
                    ext = format.split("/")[-1]
                    file_name = f"profile_{user.id}.{ext}" 
                    img_data = ContentFile(base64.b64decode(imgstr), name=file_name)
                else:
                    img_data = ContentFile(base64.b64decode(photo), name=f"profile_{user.id}.png")

                    user.profile_image.save(img_data.name, img_data, save=True)
                return Response({"message": "Profile image updated successfully"}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"message": f"Failed to decode and save image: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"message" : "Profile Updated Succesfully"} , status=status.HTTP_200_OK)

class PaymentHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            bookings = Booking.objects.filter(user=request.user)
            if not bookings.exists():
                return Response(
                    {"message": "No booking history found."},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            serializer = BookingHistorySerializer(bookings, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"message": "An error occurred while retrieving payment history."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class BookingHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            bookings = Booking.objects.filter(user=request.user)
            if not bookings.exists():
                return Response(
                    {"message": "No booking history found."},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            serializer = BookingHistorySerializer(bookings, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"message": "An error occurred while retrieving booking history."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )