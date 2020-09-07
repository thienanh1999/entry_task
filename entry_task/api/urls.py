from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .api import user, event, photo

urlpatterns = [
    # User
    url(r'^login/$', csrf_exempt(user.login)),
    url(r'^refresh/$', csrf_exempt(user.refresh)),
    url(r'^create_user/$', csrf_exempt(user.create_user)),

    # Event
    url(r'^event/(?P<event_id>\d+)/$', csrf_exempt(event.update_event)),
    url(r'^event/$', csrf_exempt(event.event)),

    # Like
    url(r'^event/(?P<event_id>\d+)/like/$', csrf_exempt(event.like)),
    url(r'^event/(?P<event_id>\d+)/unlike/$', csrf_exempt(event.unlike_event)),

    # Comment
    url(r'^event/(?P<event_id>\d+)/comment/$', csrf_exempt(event.comment)),

    # Participant
    url(r'^event/(?P<event_id>\d+)/participant/$', csrf_exempt(event.participant)),

    # Image
    url(r'^image/$', csrf_exempt(photo.upload)),
]
