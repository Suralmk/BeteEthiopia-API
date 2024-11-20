from django.db import models
# Create your models here
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

def image_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.id, filename)

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
    profile_image = models.ImageField(upload_to=image_directory_path, blank=True, null=True, default="duck.png")
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
