from django.shortcuts import render
from . models import Agent
from rest_framework.views import APIView
from rest_framework import permissions,  status, generics
from . serializers import *
class TourAgentView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Agent.objects.all()
    serializer_class = TourAgentSerializer

class TourAgentDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Agent.objects.all()
    serializer_class = TourAgentSerializer
    lookup_field = "id"

class TourAgentDestinationsView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Agent.objects.all()
    serializer_class = AgentDestinationSerializer
    lookup_field = "id"