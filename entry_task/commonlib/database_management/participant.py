from commonlib.models import Participant, Event, User
from . import utils
from django.core.paginator import Paginator


class ParticipantManagement():

    def list(self, event_id, limit=10, page=1):
        # Check if event_id exists
        if utils.get_object_or_none(Event, id=event_id) is None:
            return None

        participants = Participant.objects.filter(event_id=event_id)
        total = participants.count()
        paginator = Paginator(participants, page)

        list_of_participants = []
        try:
            for participant in paginator.page(page):
                user = utils.get_object_or_none(User, id=participant.user_id)
                if user is not None:
                    list_of_participants.append({
                        'user_id': user.id,
                        'username': user.username,
                        'fullname': user.fullname,
                    })
        except:
            pass

        response = {}
        response['list_of_participants'] = list_of_participants
        response['total'] = total
        return response

    def create(self, event_id, user_id):
        # Check if event_id exists
        if utils.get_object_or_none(Event, id=event_id) is None:
            return None

        participant = Participant.objects.filter(user_id=user_id, event_id=event_id)

        if participant.count() == 0:
            Participant.objects.create(user_id=user_id, event_id=event_id)

        total = Participant.objects.filter(event_id=event_id).count()

        return total
