# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role'] # Added role here for signup 
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username'] # For the Admin to update username