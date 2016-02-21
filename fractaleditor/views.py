from django.http import HttpResponse
from django.template import Context, loader
from fractals.models import Fractal
import re

def home(request, id = -1):
    template = loader.get_template('home.html')

    allFrac = Fractal.objects.all().order_by('-id')
    is_android = False
    if re.match('.*Android.*', request.META['HTTP_USER_AGENT']) is not None:
        is_android = True
    for fractal in allFrac:
        if fractal.thumbnail == '':
            fractal.hasthumbnail = False
        else:
            fractal.hasthumbnail = True
    context = Context({
        'fractals' : allFrac,
        'show_edit_links' : is_android
    })
    return HttpResponse(template.render(context))
