from django.conf.urls import url

from fractals import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    url(r'save', views.save),
    url(r'^$',views.index),
    url(r'^(?P<id>\d+)$', views.index)
]
