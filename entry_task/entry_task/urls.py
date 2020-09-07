"""entry_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static

from .views import user, event, photo


urlpatterns = [
    # User
    url(r'^api/user/get_salt/$', csrf_exempt(user.get_salt)),
    url(r'^api/user/login/$', csrf_exempt(user.login)),
    url(r'^api/user/create_user/$', csrf_exempt(user.create_user)),
    
    # Event
    url(r'^api/event/(?P<event_id>\d+)/$', csrf_exempt(event.update_event)),
    url(r'^api/event/$', csrf_exempt(event.event)),
    
    # Like
    url(r'^api/event/(?P<event_id>\d+)/like/$', csrf_exempt(event.like)),
    url(r'^api/event/(?P<event_id>\d+)/unlike/$', csrf_exempt(event.unlike_event)),
    
    # Comment
    url(r'^api/event/(?P<event_id>\d+)/comment/$', csrf_exempt(event.comment)),
    
    # Participant
    url(r'^api/event/(?P<event_id>\d+)/participant/$', csrf_exempt(event.participant)),
    
    # Image
    url(r'^api/image/$', csrf_exempt(photo.upload)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
