from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

class UserService():
    
    def create_user_object(self, form):
        username = form.instance.username
        email = form.instance.email
        password = form.instance.password
        user = User.objects.create_user(username, email, password)
        return user
    
    def log_user_in(self, request, username, password):
        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)