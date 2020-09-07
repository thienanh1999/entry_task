from . import utils
from django.core.paginator import Paginator
from ..models import Event
from django.forms.models import model_to_dict
import datetime
from ..database_management.event import EventManagement
from ..database_management.like import LikeManagement
from ..database_management.user import UserManagement
from ..database_management.comment import CommentManagement
from ..database_management.participant import ParticipantManagement

KEY = 'key'
HOST = 'localhost:8000'
FIELDS_TO_UPDATE = ['title', 'start', 'end', 'file', 'location', 'description', 'images']
FIELDS_TO_SORT = ['title', 'start', 'location']


def event(request):
    token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
    user_data = utils.validate_token(token, KEY, datetime.timedelta(hours=1))
    if user_data:
        if not utils.check_user(user_data['username'], user_data['password']):
            return utils.response_400('Invalid access token')
    else:
        return utils.response_400('Invalid access token')

    # Get user_id
    user = UserManagement().retrieve(username=user_data['username'])

    if request.method == 'POST':
        return create_event(request, user)
    else:
        return list_event(request)


def create_event(request, user):
    # Check admin
    if not user.is_admin:
        return utils.response_403('Admin only')

    ok, missing, data = utils.validate_fields(['title', 'start', 'end', 'location', 'category'], request)

    if not ok:
        return utils.response_400(missing)

    description = request.POST.get('description', None)
    if description is not None:
        data['description'] = description
    data['category'] = data['category'].split(',')

    event = EventManagement().create(data)

    return utils.response_200(event)


def list_event(request):
    limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)
    title = request.GET.get('title', None)

    events = Event.objects.all()
    if title is not None:
        events = events.filter(title=title)
    paginator = Paginator(events, limit)

    event_list = []
    try:
        for event in paginator.page(page):
            event_list.append(event.as_dict())
    except:
        pass

    total = events.count()
    page = int(page)
    limit = int(limit)
    next = "%s/api/event?limit=%d&page=%d" % (HOST, limit, page+1)
    previous = "%s/api/event?limit=%d&page=%d" % (HOST, limit, page-1)

    return utils.response_200({
        'total': total,
        'next': next,
        'previous': previous,
        'events': event_list,
    })


def update_event(request, event_id):
    token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
    user_data = utils.validate_token(token, KEY, datetime.timedelta(hours=1))
    if user_data:
        if not utils.check_user(user_data['username'], user_data['password']):
            return utils.response_400('Invalid access token')
    else:
        return utils.response_400('Invalid access token')

    # Get user_id
    user = UserManagement().retrieve(username=user_data['username'])
    user_id = user.id

    # Check admin
    if not user.is_admin:
        return utils.response_403('Admin only')

    kwargs = {}
    for field in FIELDS_TO_UPDATE:
        value = request.POST.get(field, None)
        if value is not None:
            kwargs[field] = value

    event = EventManagement().update(event_id=event_id, user_id=user_id, **kwargs)

    if event is None:
        return utils.response_400('Event id does not exist.')
    else:
        return utils.response_200(event)


################# LIKE #################


def like(request, event_id):
    token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
    user_data = utils.validate_token(token, KEY, datetime.timedelta(hours=1))
    if user_data:
        if not utils.check_user(user_data['username'], user_data['password']):
            return utils.response_400('Invalid access token')
    else:
        return utils.response_400('Invalid access token')

    # Get user_id
    user = UserManagement().retrieve(username=user_data['username'])
    user_id = user.id

    if request.method == 'POST':
        return like_event(event_id, user_id)
    else:
        return list_like(request, event_id)


def like_event(event_id, user_id):
    total = LikeManagement().create_or_like(event_id, user_id)

    if total is None:
        return utils.response_404('Event id does not exist.')

    return utils.response_200(total)


def list_like(request, event_id):
    limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)
    likes = LikeManagement().list(event_id, limit, page)

    if likes is None:
        return utils.response_404('Event id does not exists.')

    return utils.response_200(likes)


def unlike_event(request, event_id):
    token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
    user_data = utils.validate_token(token, KEY, datetime.timedelta(hours=1))
    if user_data:
        if not utils.check_user(user_data['username'], user_data['password']):
            return utils.response_400('Invalid access token')
    else:
        return utils.response_400('Invalid access token')

    # Get user_id
    user = UserManagement().retrieve(username=user_data['username'])
    user_id = user.id

    total = LikeManagement().unlike_event(event_id, user_id)

    if total is None:
        return utils.response_404('Event id does not exist.')

    return utils.response_200(total)


################# COMMENT #################


def comment(request, event_id):
    token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
    user_data = utils.validate_token(token, KEY, datetime.timedelta(hours=1))
    if user_data:
        if not utils.check_user(user_data['username'], user_data['password']):
            return utils.response_400('Invalid access token')
    else:
        return utils.response_400('Invalid access token')

    # Get user_id
    user = UserManagement().retrieve(username=user_data['username'])
    user_id = user.id

    if request.method == 'POST':
        return post_comment(request, event_id, user_id)
    else:
        return list_comment(request, event_id)


def post_comment(request, event_id, user_id):
    # Get comment
    ok, missing, data = utils.validate_fields(['comment'], request)
    if not ok:
        return utils.response_400(missing)

    comment = CommentManagement().create(event_id, user_id, data['comment'])

    if comment is None:
        return utils.response_404('Event id does not exist.')
    else:
        return utils.response_200(model_to_dict(comment))


def list_comment(request, event_id):
    limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)
    comments = CommentManagement().list(event_id, limit, page)

    if comments is None:
        return utils.response_404('Event id does not exist.')

    return utils.response_200(comments)


################# PARTICIPANT #################


def participant(request, event_id):
    token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
    user_data = utils.validate_token(token, KEY, datetime.timedelta(hours=1))
    if user_data:
        if not utils.check_user(user_data['username'], user_data['password']):
            return utils.response_400('Invalid access token')
    else:
        return utils.response_400('Invalid access token')

    # Get user_id
    user = UserManagement().retrieve(username=user_data['username'])
    user_id = user.id

    if request.method == 'POST':
        return participate(event_id, user_id)
    else:
        return list_participant(request, event_id)


def participate(event_id, user_id):
    total = ParticipantManagement().create(event_id, user_id)

    if total is None:
        return utils.response_404('Event id does not exist.')

    return utils.response_200(total)


def list_participant(request, event_id):
    limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)
    participants = ParticipantManagement().list(event_id, limit, page)

    if participants is None:
        return utils.response_404('Event id does not exists.')

    return utils.response_200(participants)
