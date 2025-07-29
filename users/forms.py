from django import forms 
import re
from django.contrib.auth.models import User, Group, Permission
from events.forms import StyledFormMixin
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomRegisterForm(StyledFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']


    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exist = User.objects.filter(email=email).exists()

        if email_exist:
            raise forms.ValidationError('Email already exists')
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        errors = []

        if len(password) < 8:
            errors.append('Password must be at least 8 character long')

        if not re.search(r'[A-Z]', password):
            errors.append('Password must be at least one uppercase letter.')
        
        if not re.search(r'[a-z]', password):
            errors.append('Password must be at least one lowercase letter.')
        
        if not re.search(r'[0-9]', password):
            errors.append('Password must include at least one number.')
        
        if not re.search(r'[@#$%^&+=]', password):
            errors.append('Password must be at least one special character.')
        
        if errors:
            raise forms.ValidationError(errors)

        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
            
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password did not match")
        
        return cleaned_data
        

class LoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)


class AssignRoleForm(StyledFormMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role"
    )


class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permission'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

class CustomPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['old_password'].help_text = "Enter your current password here."
            self.fields['new_password1'].help_text = "Your password can’t be too similar to your other personal information. \nYour password must contain at least 8 characters. \nYour password can’t be a commonly used password. \nYour password can’t be entirely numeric."
            self.fields['new_password2'].help_text = "Enter the same password as before, for verification."

class CustomPasswordResetForm(StyledFormMixin, PasswordResetForm):
    pass

class CustomPasswordResetConfirmForm(StyledFormMixin, SetPasswordForm):
    pass

class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_no', 'profile_image', 'website', 'designation', 'company', 'office_address', 'home_address']