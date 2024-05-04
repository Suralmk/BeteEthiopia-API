from django.contrib import admin
from . models import User, TourAgent, TourAgentImages,  Booking, Destination, DestinationImages, Price

admin.site.register(User)
admin.site.register(TourAgent)
admin.site.register(TourAgentImages)
admin.site.register(Destination)
admin.site.register(DestinationImages)
admin.site.register(Price)
admin.site.register(Booking)
