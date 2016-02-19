from django.http import HttpResponse
from django.template import Context, loader
from django.conf import settings
from models import Fractal
from django.views.decorators.csrf import csrf_exempt
import logging
import re

def index(request, id = -1):
    template = loader.get_template('fractals/index.html')
    
    numFrac = Fractal.objects.count();
    context = None
    
    if numFrac == 0:
        context = Context({
            'numPoints' : 500000,
            'name' : 'Sierpinski Pyramid',
            'serializedTransforms' : '0.5 0.0 0.0 0.0 0.0 0.5 0.0 0.0 0.0 0.0 0.5 0.0 -0.5 -0.5 -0.5 1.0 0.5 0.0 0.0 0.0 0.0 0.5 0.0 0.0 0.0 0.0 0.5 0.0 0.5 -0.5 -0.5 1.0 0.5 0.0 0.0 0.0 0.0 0.5 0.0 0.0 0.0 0.0 0.5 0.0 0.0 -0.5 0.5 1.0 0.5 0.0 0.0 0.0 0.0 0.5 0.0 0.0 0.0 0.0 0.5 0.0 0.0 0.5 0.0 1.0'
        })
    else:
        id = int(id)
        frac = Fractal.objects.get(id__exact=id)
        if frac == None:
            return HttpResponse('Fractal not found') #should be 404
        context = Context({
            'numPoints' : 500000,
            'name' : frac.name,
            'serializedTransforms' : frac.transforms
        }) 
    return HttpResponse(template.render(context))

@csrf_exempt
def save(request, id = None):
    logger = logging.getLogger('django')
    name = request.POST.get('name', '')
    serializedTransforms = request.POST.get('serializedTransforms', '')
    uploaded = request.FILES['thumbnail']
    logger.debug('Name is {0}, transforms are {1}, thumb name is {2}'.format(name, serializedTransforms, uploaded.name))

    if re.match('frac_-?[0-9]+.png$', uploaded.name) == None:
        logger.debug('Illegal thumbnail file name')
        return HttpResponse("Error: invalid thumbnail file name")

    if name == '' or serializedTransforms == '':
        return HttpResponse("Error: blank name or transforms")

    transformParts = serializedTransforms.split(' ');
    if len(transformParts) % 16 != 0:
        return HttpResponse("Error: transform count must be a multiple of 16")

    numTransforms = len(transformParts) / 16
    logger.debug('Passed initial checks, will try to save')
    try:
        filename = settings.MEDIA_ROOT + uploaded.name
        logger.debug('Trying to write thumbnail to {0}'.format(filename))
        with open(filename, 'w') as thumbfile:
            for chunk in uploaded.chunks():
                thumbfile.write(chunk)

        logger.debug('Wrote thumbnail, saving fractal to database')
        fractal = Fractal(
                          id = id,
                          name= name,
                          transformCount = numTransforms,
                          transforms = serializedTransforms,
                          thumbnailWidth = 0,
                          thumbnailHeight = 0,
                          thumbnail = uploaded.name
                          )
        fractal.save()
        logger.debug('Saved fractal to db')
    except Exception as e:
        logger.exception(e)

    return HttpResponse("Saved!")
