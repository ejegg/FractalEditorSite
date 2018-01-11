from django.http import HttpResponse
from django.template import RequestContext, loader
from fractals.models import Fractal


def home(request):
    template = loader.get_template('home.html')

    allFrac = Fractal.objects.all().order_by('-id')
    for fractal in allFrac:
        if fractal.thumbnail == '':
            fractal.hasthumbnail = False
        else:
            fractal.hasthumbnail = True
    context = {
        'fractals': allFrac
    }
    return HttpResponse(template.render(context))
