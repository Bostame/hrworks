from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    # Personal Details
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=255, blank=True, null=True)
    citizenship = models.CharField(max_length=100, blank=True, null=True)
    salutation = models.CharField(
        max_length=10,
        choices=[('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Dr.', 'Dr.'), ('Prof.', 'Prof.')],
        blank=True,
        null=True
    )

    # Contact Details
    email = models.EmailField(unique=True)
    private_email = models.EmailField(blank=True, null=True)
    office_phone = models.CharField(max_length=20, blank=True, null=True)
    private_mobile = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact = models.CharField(max_length=20, blank=True, null=True)

    # Employment Details
    current_position = models.CharField(max_length=255, blank=True, null=True)
    seniority = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    # Wage Data
    social_security_number = models.CharField(max_length=50, blank=True, null=True)
    tax_identification_number = models.CharField(max_length=50, blank=True, null=True)
    highest_school_certificate = models.CharField(max_length=255, blank=True, null=True)
    highest_professional_qualification = models.CharField(max_length=255, blank=True, null=True)
    tax_class = models.IntegerField(blank=True, null=True)
    child_allowance = models.IntegerField(blank=True, null=True)

    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        default='profile_pictures/default_profile.png', 
        blank=True, 
        null=True
    )

    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        return f"{settings.MEDIA_URL}profile_pictures/default_profile.png"  # Ensures correct URL for default image


    


    
