from rest_framework import serializers
from django.contrib.auth import get_user_model
from . models import User
from destination.models import Destination, Price, DestinationImages
from agent.models import Agent
from booking.models import Booking
from destination.models import Price, Destination
from django.contrib.auth.password_validation import validate_password



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

class AgentPriceSerializer(serializers.ModelSerializer):
    agent_id = serializers.SerializerMethodField()

    class Meta:
        model = Price
        fields =  ["price", "agent_id"]
        
    def get_agent_id(self, obj):
        id = obj.agent.id
        return  id
     
class SerachAgentSerializer(serializers.ModelSerializer):

    class Meta:
        model=Agent
        fields = [
            "id",
            "name",
            "image",
            "description",
        ]
        
class SerachDestinationSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model=Destination
        fields = [
                "id", 
                "name",
                "images",
                "location", 
                "description", 
                "weather",
                "category", 
                "accomodation",
                "price", 
            ]
        
    def get_images(self, obj):
        request = self.context.get("request")
        images = [image for image in DestinationImages.objects.filter(destination__id=obj.id).all()]

        serialized_image = ImageSerializer(
            images,  
            many=True,
            context = {"request" : request}
            ).data
        return  serialized_image
    
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
        
class BookingHistorySerializer(serializers.ModelSerializer):
    agent =  serializers.SerializerMethodField()
    destination = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = "__all__"


    def get_agent(self, obj):
        agent_id = obj.agent.id
        agent_name = obj.agent.name
        return {
            "id" : agent_id,
            "name" : agent_name
        }

    def get_destination(self, obj):
        destination_id= obj.destination.id
        destination_name = obj.destination.name
        return {
            "id" : destination_id,
            "name" : destination_name
        }

    def get_price(self, obj):
        pass

class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model =  User
        fields = ["first_name", "last_name", "email", "profile_image"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("This email is already in use by another account.")
        return value
    
class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
