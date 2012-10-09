from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from account.models import UserProfile
from django.core.exceptions import ValidationError
from django.db.models.fields.files import FieldFile
from django.contrib.auth import models

class UserProfileForm(ModelForm):
    accepted_file_types = ['image/jpeg']
    class Meta:
        model = UserProfile
        exclude = ('user')
        
    def clean_profile_image(self):
        file_object = self.cleaned_data['profile_image']
        if not isinstance(file_object, FieldFile):
            if file_object.content_type not in self.accepted_file_types:
                raise ValidationError("You can only upload jpeg files")
        return file_object

class UserUpdateForm(ModelForm):
    current_password = forms.CharField(max_length=200,widget=forms.PasswordInput(render_value=True))
    new_password = forms.CharField(max_length=200,widget=forms.PasswordInput(render_value=True))
    new_password_confirm = forms.CharField(max_length=200,widget=forms.PasswordInput(render_value=True))
    
    class Meta:
        model = User
        exclude = ('first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions', 'password')
        
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['current_password'].required = False
        self.fields['new_password'].required = False
        self.fields['new_password_confirm'].required = False
        
    def clean(self):
        cleaned_data = super(UserUpdateForm, self).clean()
        if 'new_password' not in cleaned_data and 'new_password_confirm' not in cleaned_data and 'current_password' not in cleaned_data:
            return cleaned_data
        
        current_password = cleaned_data['current_password']
        new_password = cleaned_data['new_password']
        new_password_confirm = cleaned_data['new_password_confirm']
        if not models.check_password(current_password, self.instance.password):
            raise ValidationError("Current password is incorrect")
        if not new_password or not new_password_confirm:
            raise ValidationError("Please enter and confirm a new password")
        if new_password != new_password_confirm:
            raise ValidationError("New passwords do not match")
        
        return cleaned_data
    
class UserForm(ModelForm):
    password = forms.CharField(max_length=200,widget=forms.PasswordInput(render_value=True))
    password_confirm = forms.CharField(max_length=200,widget=forms.PasswordInput(render_value=True))
    
    class Meta:
        model = User
        exclude = ('first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions')
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        if 'password' not in cleaned_data:
            raise ValidationError("Please enter a password")
        if 'password_confirm' not in cleaned_data:
            raise ValidationError("Please enter a password")
        
        password = cleaned_data['password']
        password_confirm = cleaned_data['password_confirm']
        
        if password != password_confirm:
            raise ValidationError("Passwords do not match")
        
        return cleaned_data
