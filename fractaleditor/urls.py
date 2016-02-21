from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fractaleditor.views.home', name='home'),
    # url(r'^fractaleditor/', include('fractaleditor.foo.urls')),
    url(r'^fractal/', include('fractals.urls')),
    url(r'^$', 'fractaleditor.views.home', name='home'),
    url(r'^app$', 'fractals.views.app_link'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
