from django.db import models
# Create your models here
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

def image_directory_path(instance, filename):
    return 'image_{0}/{1}'.format(instance.destination.name, filename)

def agent_directory_path(instance, filename):
    return 'agent_{0}/{1}'.format(instance.agent.name, filename)

class UserManager(BaseUserManager):
  def create_user (self, email,  first_name, last_name,password=None ,is_active=True, is_staff=False, is_admin=False):
      if not email:
          raise ValueError("User must have email")
      if not password:
          raise ValueError("User must have password")
      if not first_name:
          raise ValueError("User must have first name")
      if not last_name:
          raise ValueError("User must have last name")

      email = self.normalize_email(email)
      user = self.model( 
          email=email,
          first_name=first_name,
          last_name=last_name
      )
      user.set_password(password)
      user.active = is_active
      user.staff = is_staff
      user.admin = is_admin
      user.save()
      return user
  
  def create_staffuser(self, email, first_name, last_name, password=None):
      if not email:
          raise ValueError("User must have email")
      if not password:
          raise ValueError("User must have password")
      if not first_name:
          raise ValueError("User must have first name")
      if not last_name:
          raise ValueError("User must have last name")
      
      user = self.create_user(
          email, 
          first_name,
          last_name,
          password=password,
          is_staff=True
      )
      return user
  def create_superuser(self, first_name, last_name, email ,password=None): 
      if not email:
          raise ValueError("User must have email")
      if not password:
          raise ValueError("User must have password")
      if not first_name:
          raise ValueError("User must have first name")
      if not last_name:
          raise ValueError("User must have last name")
      
      user = self.create_user(
            email, 
          first_name,
          last_name,
          password=password,
          is_staff=True,
          is_admin=True,
      )
      return user

class User(AbstractBaseUser, PermissionsMixin):
    email =   models.EmailField(unique=True,  max_length=255)
    first_name = models.CharField(max_length=150, null=False, default="")
    last_name = models.CharField(max_length=150, null=False, default="")
    profile_image = models.ImageField(upload_to=user_directory_path, blank=True, null=True, default="duck.png")
    active =  models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', "last_name"]
    objects  = UserManager()

    def __str__(self):
        return self.email
    
    def get_short_name(self):
        return self.first_name
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active
      
class TourAgent(models.Model):
    name = models.CharField(max_length=70)
    # image = models.ImageField(upload_to=agent_directory_path, default="duck.png")
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    
class TourAgentImages(models.Model):
    agent = models.ForeignKey(TourAgent, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=agent_directory_path)

    def __str__(self):
        return self.agent.name

class Destination(models.Model):
    destination_category = (
        ('culture', 'Culture'),
        ('food', 'Food'),
        ('wildlife', 'Wildlife'),
        ('nature', 'Nature')    
    )
    name = models.CharField(max_length=70)
    location = models.CharField(max_length=70)
    description = models.CharField(max_length=500)
    weather = models.CharField(max_length=500)
    accomodation = models.CharField(max_length=500)
    category = models.CharField(max_length=15, choices=destination_category, default="All")
    #image = models.ImageField(upload_to=image_directory_path, default="duck.png")
    agent = models.ManyToManyField(TourAgent, related_name="agent_destination")

    def __str__(self):
        return self.name

    def get_template(self, id):
        image = self.images.first()
        print(image)
        return self.images.first()

class DestinationImages(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=image_directory_path)

    def __str__(self):
        return self.destination.name
    
class Price(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="destination_price")
    agent = models.ForeignKey(TourAgent, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return str(self.agent ) + " / " + str(self.destination) + " / " + str(self.price)
    
class Booking(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="booking_destination")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booking_user")
    agent = models.ForeignKey(TourAgent, on_delete=models.CASCADE, related_name="booking_agent")
    phone = models.IntegerField()
    country = models.CharField(max_length=100)
    guest_number = models.IntegerField()
    special_need = models.TextField() 
    for_date = models.DateTimeField()
    booking_date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)


