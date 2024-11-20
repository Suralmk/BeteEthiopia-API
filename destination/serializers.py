from rest_framework import serializers
from . models import Destination, Price, DestinationImages, DestinationCategory


class AgentPriceSerializer(serializers.ModelSerializer):
    agent_id = serializers.SerializerMethodField()

    class Meta:
        model = Price
        fields =  ["price", "destination", "agent_id"]
        
    def get_agent_id(self, obj):
        id = obj.agent.id
        return  id
    
class ImageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.ImageField()

    def get_photo_url(self, obj):
        request = self.context.get("request")
        url = obj.fingerprint.url
        return request.build_absolute_url(url) 
    
class DestinationCategorySerializer(serializers.ModelSerializer):
    class Meta:
            model = DestinationCategory
            fields =  "__all__"

class DestinationSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Destination
        fields = [
                "id", 
                "name",
                "images",
                "location", 
                "description", 
                "weather",
                "category", 
                "accomodation",
                "price" 
            ]

    def get_price(self, obj):
        request = self.context.get("request")
        agent_id = self.context.get("id")

        if agent_id:
            price = Price.objects.filter(destination=obj.id, agent=agent_id)
            agent_price = AgentPriceSerializer(
                    price, 
                    many=True, 
                    context = {"request" : request}
                ).data

            return agent_price
        else:
            prices = [price for  price in obj.destination_price.all()]
            agents_price = AgentPriceSerializer(
                                        prices, 
                                        many=True, 
                                        context = {"request" : request}
                                                ).data

            return agents_price
        
    def get_images(self, obj):

        request = self.context.get("request")
        images = [image for image in DestinationImages.objects.filter(destination__id=obj.id).all()]

        serialized_image = ImageSerializer(
            images,  
            many=True,
            context = {"request" : request}
            ).data
        return  serialized_image
        
