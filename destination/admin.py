from django.contrib import admin
from . models import Destination, DestinationImages, Price, DestinationCategory

admin.site.register(Destination)
admin.site.register(DestinationImages)
admin.site.register(Price)
admin.site.register(DestinationCategory)