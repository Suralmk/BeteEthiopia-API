from django.db import models
from api.models import User
from agent.models import Agent
from destination.models import Destination

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booking_user")
    phone_no = models.IntegerField()
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="booking_agent")
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="booking_destination")
    nationality = models.CharField(max_length=100)
    guest_number = models.IntegerField()
    special_request = models.TextField(blank=True, null=True) 
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking by {self.user.email} for {self.destination}"

    class Meta:
        ordering = ['start_date']
