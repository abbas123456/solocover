from django.http import HttpResponse
from competition.models import Competition
from django.template import Context, loader

def list(request):              
    competitions = Competition.objects.all().order_by('-end_date')
    bindings = Context({
        'competitions': competitions,                        
    })
    template = loader.get_template('competition/list.html')
    return HttpResponse(template.render(context=bindings));