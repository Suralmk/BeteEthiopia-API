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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name","email", "profile_image"]

    def get_photo_url(self, obj):
        request = self.context.get("request")
        url = obj.fingerprint.url
        return request.build_absolute_url(url) 
    
class TourAgentSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="agent_detail",
        lookup_field="id"
    )
    class Meta:
        model = TourAgent
        fields =  ["detail_url", "name", "description", "image"]

class AgentPriceSerializer(serializers.ModelSerializer):
    agent_url = serializers.SerializerMethodField()

    class Meta:
        model = Price
        fields =  ["price", "agent_url"]
        
    # This part needs to be updated
    def get_agent_url(self, obj):
        id = obj.agent.id
        return  f"http://127.0.0.1:1200/api/agents/{id}/"
    
class DestinationSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="destination_detail",
        lookup_field="id"
    )
    agent_price = serializers.SerializerMethodField()
    class Meta:
        model = Destination
        fields = ["detail_url", "name", "location", "description", "weather", "accomodation", "agent_price"]

    def get_agent_price(self, obj):
        request = self.context.get("request") 
        prices = []
        for price in obj.destination_price.all():
            prices.append(price)
        agent_price = AgentPriceSerializer(prices, many=True, context = {"request" : request}).data
        return agent_price