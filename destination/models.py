from django.db import models
from agent.models import Agent

def destination_directory_path(instance, filename):
    return 'image_{0}/{1}'.format(instance.destination.name, filename)

class DestinationCategory(models.Model):
    category = models.CharField(default="", null=True, max_length=50)

    def __str__(self):
        return self.category

class Destination(models.Model):
    name = models.CharField(max_length=70)
    location = models.CharField(max_length=70)
    description = models.CharField(max_length=500)
    weather = models.CharField(max_length=500)
    accomodation = models.CharField(max_length=500)
    category = models.ManyToManyField(DestinationCategory, related_name="destination_category")
    agent = models.ManyToManyField(Agent, related_name="agent_destination")

    def __str__(self):
        return self.name

class DestinationImages(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=destination_directory_path)

    def __str__(self):
        return self.destination.name
  
class Price(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="destination_price")
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return str(self.agent ) + " / " + str(self.destination) + " / " + str(self.price)


