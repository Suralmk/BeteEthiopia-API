from rest_framework import serializers
from . models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

    def validate(self, attrs):
        # Validate start_date and end_date
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(

                {"error": "Start date cannot be after the end date."}
            )

        # Optional: Additional validation can go here
        return attrs
