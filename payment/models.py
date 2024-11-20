from django.db import models
from api.models import User
from booking.models import Booking
# Create your models here.

class PaymentHistory(models.Model):
    booking = models.ForeignKey(Booking, related_name="booking_price", on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, related_name="user_payment", on_delete=models.DO_NOTHING, default="", null=True)
    amount = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.booking.user.first_name +  " " + str(self.amount)