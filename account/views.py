from django.contrib.auth.models import User
from django.views.generic import CreateView,UpdateView
from account.forms import UserForm, UserProfileForm, UserUpdateForm
from account.services import UserService
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from account.models import UserProfile
from django.contrib import messages

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

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['user_profile_form'] = UserProfileForm(instance=self.request.user.get_profile())
        return context
    
    def get_object(self):
        return self.request.user
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        user = form.save()
        user_profile_form = UserProfileForm(self.request.POST, self.request.FILES, instance=user.get_profile())
        if user_profile_form.is_valid():
            user_profile_form.save()
        else:
            return render_to_response('auth/user_update_form.html', {'form': form, 'user_profile_form' : user_profile_form}, context_instance=RequestContext(self.request))
        if form.cleaned_data['new_password']:
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            return HttpResponseRedirect(reverse('songthread_list'))
        else:
            return HttpResponseRedirect(reverse('songthread_list'))