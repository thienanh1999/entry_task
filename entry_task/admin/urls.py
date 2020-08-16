from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    url(r'^admin/login/$', csrf_exempt(views.login)),
    url(r'^admin/create_event/$', csrf_exempt(views.create_event)),
    url(r'^admin/upload/$', csrf_exempt(views.upload)),
    url(r'^admin/update/$', csrf_exempt(views.update)),
]
