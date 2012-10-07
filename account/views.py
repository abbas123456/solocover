from django.contrib.auth.models import User
from django.views.generic import CreateView,UpdateView
from account.forms import UserForm, UserUpdateForm
from account.services import UserService
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class UserCreateView(CreateView):
    form_class = UserForm
    model = User
    template_name = 'auth/user_form.html'
    
    def get(self, request, *args, **kwargs):
        form = UserForm()
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('songthread_list'))
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))
    
    def form_valid(self, form):
        user_service = UserService()
        user_service.create_user_object(form)
        user_service.log_user_in(self.request, form.instance.username, form.instance.password)
        return HttpResponseRedirect(reverse('songthread_list'))
        
class UserUpdateView(UpdateView):
    model = User
    template_name_suffix = '_update_form'
    form_class = UserUpdateForm

    def get_object(self):
        return self.request.user
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(*args, **kwargs)