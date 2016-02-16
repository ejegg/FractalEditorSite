from django.http import HttpResponse
from django.template import Context, loader
from models import Fractal
from django.views.decorators.csrf import csrf_exempt
import logging

def index(request, id = -1):
    template = loader.get_template('fractals/index.html')
    
    allFrac = Fractal.objects.all();
    context = None
    
    if len(allFrac) == 0:
        context = Context({
            'numPoints' : 200000,
            'name' : 'Sierpinski Pyramid',
            'serializedTransforms' : '0.5 0.0 0.0 0.0 0.0 0.5 0.0 0.0 0.0 0.0 0.5 0.0 -0.5 -0.5 -0.5 1.0 0.5 0.0 0.0 0.0 0.0 0.5 0.0 0.0 0.0 0.0 0.5 0.0 0.5 -0.5 -0.5 1.0 0.5 0.0 0.0 0.0 0.0 0.5 0.0 0.0 0.0 0.0 0.5 0.0 0.0 -0.5 0.5 1.0 0.5 0.0 0.0 0.0 0.0 0.5 0.0 0.0 0.0 0.0 0.5 0.0 0.0 0.5 0.0 1.0'
        })
    else:
        frac = allFrac.order_by('-id')[0]
        context = Context({
            'numPoints' : 200000,
            'name' : frac.name,
            'serializedTransforms' : frac.transforms
        }) 
    return HttpResponse(template.render(context))

@csrf_exempt
def save(request, id = None):
    logger = logging.getLogger('django')
    name = request.POST.get('name', '')
    serializedTransforms = request.POST.get('serializedTransforms', '')
    logger.debug('Name is {0}, transforms are {1}'.format(name, serializedTransforms))
    if name == '' or serializedTransforms == '':
        return HttpResponse("Error: blank name or transforms")
    
    transformParts = serializedTransforms.split(' ');
    if len(transformParts) % 16 != 0:
        return HttpResponse("Error: transform count must be a multiple of 16")
    
    numTransforms = len(transformParts) / 16 
    
    fractal = Fractal(
                      id = id,
                      name= name,
                      transformCount = numTransforms, 
                      transforms = serializedTransforms,
                      thumbnailWidth = 0,
                      thumbnailHeight = 0
                      )
    try:
        fractal.save()
    except Exception as e:
        logger.exception(e)
    
    return HttpResponse("Saved!")
