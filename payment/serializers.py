from rest_framework import serializers
from .models import PaymentHistory
from booking.serializers import BookingSerializer
from api.serializers import UserSerializer  # Import User serializer if available

class PaymentHistorySerializer(serializers.ModelSerializer):
    booking = BookingSerializer()  # Nested serializer for Booking details
    user = serializers.SerializerMethodField()  # Fetching user details

    class Meta:
        model = PaymentHistory
        fields = "__all__"

    def get_user(self, obj):
        # Assuming `UserSerializer` is defined in your `api.serializers`
        from api.serializers import UserSerializer  # Import it here to avoid circular import
        serializer = UserSerializer(obj.user)
        return serializer.data
