from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    place_of_birth = forms.CharField(max_length=255)
    citizenship = forms.CharField(max_length=100)
    salutation = forms.ChoiceField(choices=[('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Dr.', 'Dr.'), ('Prof.', 'Prof.')])

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

    # New Fields (for Address, Bank, Children, and Health Insurance)
    address = forms.CharField(max_length=255, required=False)
    bank_account = forms.CharField(max_length=34, required=False)
    child_name = forms.CharField(max_length=255, required=False)
    child_birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    health_insurance = forms.CharField(max_length=255, required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'profile_picture', 'salutation', 'date_of_birth', 'place_of_birth',
            'citizenship', 'email', 'private_email', 'office_phone', 'private_mobile', 'emergency_contact',
            'current_position', 'seniority', 'start_date', 'end_date', 'social_security_number',
            'tax_identification_number', 'highest_school_certificate', 'highest_professional_qualification',
            'tax_class', 'child_allowance', 'address', 'bank_account', 'child_name', 'child_birthdate', 'health_insurance',
            'password1', 'password2'
        ]


class UserEditForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    child_birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = CustomUser
        fields = [
            'profile_picture', 'first_name', 'last_name', 'salutation', 'date_of_birth', 'place_of_birth', 'citizenship',
            'private_email', 'office_phone', 'private_mobile', 'emergency_contact',
            'current_position', 'seniority', 'start_date', 'end_date',
            'social_security_number', 'tax_identification_number', 'highest_school_certificate', 
            'highest_professional_qualification', 'tax_class', 'child_allowance',
            'address', 'bank_account', 'child_name', 'child_birthdate', 'health_insurance'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'child_birthdate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

