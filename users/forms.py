from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'address', 'role']

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role == 'Superadmin' and CustomUser.objects.filter(role='Superadmin').exists():
            raise ValidationError('There can only be one Superadmin.')
        return role

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Enter your email", max_length=254)
