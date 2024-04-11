from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import permissions,  status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from . serializers import UserSerializer, SignUpSerializer, TourAgentSerializer, DestinationSerializer
from . models import TourAgent, TourAgentImages, Destination, DestinationImages, User

from . utils import send_otp
@api_view(["GET"])
def home(request):
    return Response({"message" : "sdadsad" } ,status=200)

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
        return Response({"error": "Email does not exist"})
    data = {
            "message": "Otp succesfully send"
    }
    otp = send_otp(email)
    if otp is not None:
        user.otp = otp
        user.save()
        data["email_sent"] = True
    return Response(data, status=status.HTTP_200_OK)

class TourAgentView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = TourAgent.objects.all()
    serializer_class = TourAgentSerializer

class TourAgentDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = TourAgent.objects.all()
    serializer_class = TourAgentSerializer
    lookup_field = "id"

class DestinationView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    lookup_field = "id"