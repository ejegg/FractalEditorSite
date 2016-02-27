from django.conf import settings
from django.http import HttpRequest

def template_vars(request):
    return {
        'footer_text' : settings.FOOTER_TEXT,
        'app_link' : settings.APP_LINK,
    }
