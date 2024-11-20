from rest_framework import serializers
from . models import Agent, AgentImages
from destination.models import Price, Destination
from destination.serializers import DestinationSerializer

class ImageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.ImageField()

    def get_photo_url(self, obj):
        request = self.context.get("request")
        url = obj.fingerprint.url
        return request.build_absolute_url(url) 
    
class TourAgentSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields =  ["id", "name", "description", "images"]

    def get_images(self, obj):
        request = self.context.get("request")
        images = [image for image in  AgentImages.objects.filter(agent__id=obj.id).all()]
        serialized_images = ImageSerializer(images, many=True, context = {"request" : request}).data

        return serialized_images

class AgentPriceSerializer(serializers.ModelSerializer):
    agent_id = serializers.SerializerMethodField()

    class Meta:
        model = Price
        fields =  ["price", "agent_id"]
        
    def get_agent_id(self, obj):
        id = obj.agent.id
        return  id
    
class AgentDestinationSerializer(serializers.ModelSerializer):
    agent = serializers.SerializerMethodField()
    destination =  serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = ["agent", "destination"]

    def get_agent(self, obj):
        return obj.id
    
    def get_destination(self, obj):
        request = self.context.get("request") 
        destination = Destination.objects.filter(agent=obj.id).all()
        serialized_destination = DestinationSerializer(
            destination,
            many=True, 
            context = {
                "request" : request,
                "id" : obj.id
                }
        ).data

        return serialized_destination