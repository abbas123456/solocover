from django.http import HttpResponse
from competition.models import Competition
from django.template import RequestContext, loader

def list(request):              
    competitions = Competition.objects.all().order_by('-end_date')
    bindings = RequestContext(request, {
        'competitions': competitions,                        
    })
    template = loader.get_template('competition/list.html')
    return HttpResponse(template.render(context=bindings));