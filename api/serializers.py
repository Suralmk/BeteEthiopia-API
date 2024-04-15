from rest_framework import serializers
from django.contrib.auth import get_user_model
from . models import User, TourAgent, Destination, DestinationImages, TourAgentImages, Price
from rest_framework import reverse


class SignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        print(validated_data)
        first_name= validated_data.get("first_name").lower()
        last_name = validated_data.get("last_name").lower()
        email = validated_data.get("email").lower()
        password = validated_data.get("password")
        user = User.objects.create(
            first_name= first_name,
            last_name =last_name,
            email =email
        )
        user.set_password(password)
        user.save()
        return user
    
class ImageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.ImageField()

    def get_photo_url(self, obj):
        request = self.context.get("request")
        url = obj.fingerprint.url
        return request.build_absolute_url(url) 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name","email", "profile_image"]

    def get_photo_url(self, obj):
        request = self.context.get("request")
        url = obj.fingerprint.url
        return request.build_absolute_url(url) 
    
class TourAgentSerializer(serializers.ModelSerializer):

    images = serializers.SerializerMethodField()
    class Meta:
        model = TourAgent
        fields =  ["id", "name", "description", "images"]

    def get_images(self, obj):
        request = self.context.get("request")
        images = [image for image in  TourAgentImages.objects.filter(agent__id=obj.id).all()]
        serialized_images = ImageSerializer(images, many=True, context = {"request" : request}).data
        return serialized_images

class AgentPriceSerializer(serializers.ModelSerializer):
    agent_id = serializers.SerializerMethodField()

    class Meta:
        model = Price
        fields =  ["price", "agent_id"]
        
    # This part needs to be updated 
    def get_agent_id(self, obj):
        id = obj.agent.id
        return  id
    
class DestinationSerializer(serializers.ModelSerializer):

    agent_price = serializers.SerializerMethodField()
    class Meta:
        model = Destination
        fields = ["id", "name","image", "location", "description", "weather","category", "accomodation", "agent_price"]

    def get_agent_price(self, obj):
        request = self.context.get("request") 
        prices = []
        for price in obj.destination_price.all():
            prices.append(price)
        agent_price = AgentPriceSerializer(prices, many=True, context = {"request" : request}).data
        return agent_price
    