from rest_framework import permissions,  status, generics, views
from rest_framework.response import Response
from . serializers import *
from . models import Destination
from agent.models import Agent

class DestinationView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    lookup_field = "id" 

class CategoriesView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = DestinationCategory.objects.all()
    serializer_class = DestinationCategorySerializer

class PricesView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, destination_id, agent_id):
        try:
            agent = Agent.objects.get(id=agent_id)
            destination = Destination.objects.get(id=destination_id)
            price_entry = Price.objects.get(destination=destination, agent=agent)
            data = {
                "price": price_entry.price,
            }
            return Response(data, status=status.HTTP_200_OK)
        except Price.DoesNotExist:
            return Response({"message": "Price not found for the given agent and destination."}, status=status.HTTP_404_NOT_FOUND)