from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
# Create your models here.



def validate_phone_number(value):
    if not value.isdigit() or len(value) != 11:
        raise ValidationError("Phone number must be exactly 11 digits.")
    

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images', blank=True, default='profile_images/default-profile-image.jpg')
    phone_no = models.CharField(max_length=15, validators=[validate_phone_number], blank=True, null=True)
    
    website = models.URLField(blank=True, null=True)
    designation = models.CharField(blank=True, null=True)
    company = models.CharField(blank=True, null=True)
    office_address = models.TextField(blank=True, null=True)
    home_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username