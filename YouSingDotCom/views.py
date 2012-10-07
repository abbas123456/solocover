from django.views.generic.base import TemplateView
from account.forms import UserForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from account.services import UserService
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class LandingPageView(TemplateView):

    template_name = "landing.html"
    
    def get(self, request, *args, **kwargs):
        form = UserForm()
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('songthread_list'))
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))
        
    def get_context_data(self, **kwargs):
        context = super(LandingPageView, self).get_context_data(**kwargs)
        context['form'] = UserForm()
        return context

    def post(self, request, *args, **kwargs):
        form = UserForm(data=request.POST)
        if form.is_valid():
            user_service = UserService()
            user_service.create_user_object(form)
            user_service.log_user_in(request, form.instance.username, form.instance.password)
            return HttpResponseRedirect(reverse('songthread_list'))
        else:
            return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))
