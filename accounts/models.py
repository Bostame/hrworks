from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta

class CustomUser(AbstractUser):
    # Role Choices
    CEO = 'CEO'
    HR = 'HR'
    TEAM_LEAD = 'Team Lead'
    DEPUTY_LEAD = 'Deputy Lead'
    EMPLOYEE = 'Employee'

    ROLE_CHOICES = [
        (CEO, 'CEO'),
        (HR, 'HR'),
        (TEAM_LEAD, 'Team Lead'),
        (DEPUTY_LEAD, 'Deputy Lead'),
        (EMPLOYEE, 'Employee'),
    ]

    # Role Field
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=EMPLOYEE)

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

    # Address
    address = models.CharField(max_length=255, blank=True, null=True)

    # Bank Account
    bank_account = models.CharField(max_length=34, blank=True, null=True)

    # Children
    child_name = models.CharField(max_length=255, blank=True, null=True)
    child_birthdate = models.DateField(blank=True, null=True)

    # Health Insurance
    health_insurance = models.CharField(max_length=255, blank=True, null=True)

    # **Vacation Tracking**
    vacation_balance = models.IntegerField(default=30)  # Start with 30 vacation days

    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        return f"{settings.MEDIA_URL}profile_pictures/default_profile.png"  # Ensures correct URL for default image

    def deduct_vacation(self, days=1):
        """Deducts vacation days if available."""
        if self.vacation_balance > 0:
            self.vacation_balance -= days
            self.save()

    # Role-based permissions
    def is_hr(self):
        return self.role == self.HR or self.is_superuser  # Superusers have all roles

    def is_team_lead(self):
        return self.role == self.TEAM_LEAD or self.is_superuser

    def is_deputy_lead(self):
        return self.role == self.DEPUTY_LEAD or self.is_superuser

    def is_ceo(self):
        return self.role == self.CEO or self.is_superuser

    def has_admin_privileges(self):
        """Superusers and CEOs have full access to manage everything."""
        return self.is_superuser or self.role == self.CEO or self.role == self.HR

    def __str__(self):
        return f"{self.username} - {self.role}"


class TimeTracking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=now)
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    overtime = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def calculate_hours(self):
        """Calculates total hours worked for the day considering multiple clock-ins."""
        if self.clock_in and self.clock_out:
            worked_hours = (self.clock_out - self.clock_in).total_seconds() / 3600  # Convert to hours
            self.total_hours += round(worked_hours, 2)  # Accumulate total hours
            self.overtime = max(0, self.total_hours - 8)  # Overtime calculation
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.total_hours} hours"


class Event(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    event_type = models.CharField(
        max_length=50,
        choices=[
            ("Meeting", "Meeting"),
            ("Work Shift", "Work Shift"),
            ("General", "General"),
            ("Holiday", "Holiday"),
        ]
    )
    location = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.title} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"