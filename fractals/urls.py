from django.conf.urls import patterns, url

from fractals import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fractaleditor.views.home', name='home'),
    # url(r'^fractaleditor/', include('fractaleditor.foo.urls')),
    
    url(r'save', views.save),
    url(r'^$',views.index),
    url(r'^(?P<id>\d+)$', views.index)
)
