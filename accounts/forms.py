from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from accounts.models import Event

class UserRegistrationForm(UserCreationForm):
    """Form for registering a new user."""
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)
    profile_picture = forms.ImageField(required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    place_of_birth = forms.CharField(max_length=255, required=False)
    citizenship = forms.CharField(max_length=100, required=False)
    salutation = forms.ChoiceField(choices=[('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Dr.', 'Dr.'), ('Prof.', 'Prof.')], required=False)

    # Contact Details
    private_email = forms.EmailField(required=False)
    office_phone = forms.CharField(max_length=20, required=False)
    private_mobile = forms.CharField(max_length=20, required=False)
    emergency_contact = forms.CharField(max_length=20, required=False)

    # Employment Details
    current_position = forms.CharField(max_length=255, required=False)
    seniority = forms.CharField(max_length=100, required=False)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    # Wage Data
    social_security_number = forms.CharField(max_length=50, required=False)
    tax_identification_number = forms.CharField(max_length=50, required=False)
    highest_school_certificate = forms.CharField(max_length=255, required=False)
    highest_professional_qualification = forms.CharField(max_length=255, required=False)
    tax_class = forms.IntegerField(required=False)
    child_allowance = forms.IntegerField(required=False)

    # Address, Bank, Children, and Health Insurance
    address = forms.CharField(max_length=255, required=False)
    bank_account = forms.CharField(max_length=34, required=False)
    child_name = forms.CharField(max_length=255, required=False)
    child_birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    health_insurance = forms.CharField(max_length=255, required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'profile_picture', 'salutation', 'role', 'date_of_birth', 'place_of_birth',
            'citizenship', 'email', 'private_email', 'office_phone', 'private_mobile', 'emergency_contact',
            'current_position', 'seniority', 'start_date', 'end_date', 'social_security_number',
            'tax_identification_number', 'highest_school_certificate', 'highest_professional_qualification',
            'tax_class', 'child_allowance', 'address', 'bank_account', 'child_name', 'child_birthdate', 'health_insurance',
            'password1', 'password2'
        ]


class UserEditForm(forms.ModelForm):
    """Form for editing user details, with dynamic role visibility based on editor privileges."""
    
    profile_picture = forms.ImageField(required=False)
    child_birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop('editor', None)  # Capture the logged-in user (editor)
        super().__init__(*args, **kwargs)

        # ✅ Only show role field if the editor is HR, CEO, or Superuser
        if self.editor and (self.editor.is_superuser or self.editor.role in ['HR', 'CEO']):
            self.fields['role'] = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'profile_picture', 'first_name', 'last_name', 'salutation', 'role', 'date_of_birth', 'place_of_birth', 
            'citizenship', 'email', 'private_email', 'office_phone', 'private_mobile', 'emergency_contact',
            'current_position', 'seniority', 'start_date', 'end_date', 'social_security_number', 
            'tax_identification_number', 'highest_school_certificate', 'highest_professional_qualification', 
            'tax_class', 'child_allowance', 'address', 'bank_account', 'child_name', 'child_birthdate', 
            'health_insurance'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'child_birthdate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class EventForm(forms.ModelForm):
    """Form for adding events to the company calendar."""
    
    class Meta:
        model = Event
        fields = ['title', 'event_type', 'start_time', 'end_time', 'location']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }