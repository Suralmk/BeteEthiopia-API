from django.contrib import admin
from . models import User, TourAgent, TourAgentImages, Destination, DestinationImages, Price

admin.site.register(User)
admin.site.register(TourAgent)
admin.site.register(TourAgentImages)
admin.site.register(Destination)
admin.site.register(DestinationImages)
admin.site.register(Price)
