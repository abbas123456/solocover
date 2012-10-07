from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from account.models import UserProfile
from django.core.exceptions import ValidationError

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user')

class UserForm(ModelForm):
    password = forms.CharField(max_length=200,widget=forms.PasswordInput(render_value=True))
    password_confirm = forms.CharField(max_length=200,widget=forms.PasswordInput(render_value=True))
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        
    class Meta:
        model = User
        exclude = ('first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions')
    
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
