from django.db import models
# Create your models here
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save, post_delete

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

def image_directory_path(instance, filename):
    return 'image_{0}/{1}'.format(instance.destination.name, filename)

def agent_directory_path(instance, filename):
    return 'agent_{0}/{1}'.format(instance.name, filename)

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
      

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE ,related_name="profie_owner")
#     first_name = models.CharField(max_length=100, default='Unknown', null=True, blank=True)
#     last_name = models.CharField(max_length=100, default='Name', null=True, blank=True)
#     profile_pic = models.ImageField(null=True, upload_to=user_directory_path, default="default_profile.png", blank=True)
#     bg_pic = models.ImageField(upload_to=user_directory_path, null=True, default="default_bg.png", blank=True)
#     bio = models.CharField(max_length=200, null=True, default="", blank=True)
#     location = models.CharField(max_length=100, null=True, blank=True)
#     birth_date = models.DateField(null=True, blank=True)
#     phone = models.CharField(max_length=13, null=True, blank=True)
#     follower = models.ManyToManyField(User, related_name="following" , blank=True)
#     personal_intrests = models.CharField(null=True, max_length=200, blank=True)

#         # print(request.user.following.all())
#         # print(" followers " + str(profile.follower.all()))
#     def __str__(self):
#         return self.user.username
    
#     def get_absolute_url(self):
#         return reverse('profile', args=[str(self.user.username)])
    
#     def get_total_follower(self):
#         return self.follower.count()
    
#     def get_full_name(self):
#         return str(self.first_name) + " "+ str(self.last_name)

class TourAgent(models.Model):
    name = models.CharField(max_length=70)
    image = models.ImageField(upload_to=agent_directory_path, default="duck.png")
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    
class TourAgentImages(models.Model):
    agent = models.ForeignKey(TourAgent, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=agent_directory_path)

    def __str__(self):
        return self.agent.name

class Destination(models.Model):
    name = models.CharField(max_length=70)
    location = models.CharField(max_length=70)
    description = models.CharField(max_length=500)
    weather = models.CharField(max_length=500)
    accomodation = models.CharField(max_length=500)
    agent = models.ManyToManyField(TourAgent, related_name="agent_destination")

    def __str__(self):
        return self.name


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