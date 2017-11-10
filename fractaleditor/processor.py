from django.conf import settings

import re


def template_vars(request):
    is_android = False
    if re.match('.*Android.*', request.META['HTTP_USER_AGENT']) is not None:
        is_android = True
    return {
        'footer_text': settings.FOOTER_TEXT,
        'app_link': settings.APP_LINK,
        'show_edit_links': is_android,
    }
