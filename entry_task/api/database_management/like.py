from ..models import Like, Event, User
from . import utils
from django.core.paginator import Paginator


class LikeManagement():

    def list(self, event_id, limit=10, page=1):
        # Check if event_id exists
        if utils.get_object_or_none(Event, id=event_id) is None:
            return None

        likes = Like.objects.filter(event_id=event_id, is_deleted=False)
        total = likes.count()
        paginator = Paginator(likes, limit)

        list_of_likes = []
        try:
            for like in paginator.page(page):
                user = utils.get_object_or_none(User, id=like.user_id)
                if user is not None:
                    list_of_likes.append({
                        'user_id': user.id,
                        'username': user.username,
                        'fullname': user.fullname,
                    })
        except:
            pass

        response = {}
        response['total'] = total
        response['list_of_like'] = list_of_likes
        return response

    def create_or_like(self, event_id, user_id):
        # Check if event_id exists
        if utils.get_object_or_none(Event, id=event_id) is None or utils.get_object_or_none(User, id=user_id) is None:
            return None

        like = Like.objects.filter(user_id=user_id, event_id=event_id)

        if like.count() == 0:
            Like.objects.create(user_id=user_id, event_id=event_id)
        else:
            like.update(is_deleted=False)

        total = Like.objects.filter(event_id=event_id, is_deleted=False).count()

        return total

    def unlike_event(self, event_id, user_id):
        # Check if event_id exists
        if utils.get_object_or_none(Event, id=event_id) is None or utils.get_object_or_none(User, id=user_id) is None:
            return None

        like = Like.objects.filter(user_id=user_id, event_id=event_id)

        if like.count() != 0:
            like.update(is_deleted=True)

        total = Like.objects.filter(event_id=event_id, is_deleted=False).count()

        return total
