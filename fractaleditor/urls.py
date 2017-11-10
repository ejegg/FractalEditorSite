from django.conf.urls import include, url
import django.views.static
import fractaleditor.views
import fractals.views
import os.path

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
project_root = os.path.dirname(os.path.dirname(__file__))
urlpatterns = [
    url(r'^fractal/', include('fractals.urls')),
    url(r'^$', fractaleditor.views.home, name='home'),
    url(r'^app$', fractals.views.app_link),
    url(r'^(?P<path>android-chrome-[0-9x]+\.png|apple-touch-icon-[0-9a-z]+\.png|' +
            r'browserconfig.xml|favicon-[0-9x]+\.png|favicon.ico|manifest.json|' +
            r'safari-pinned-tab.svg|mstile-[0-9x]+.png|.well-known/.*)$',
        django.views.static.serve, {
            'document_root': project_root + '/static'
        }),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
