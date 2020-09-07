from ..models import Comment, Event, User
from . import utils
from django.core.paginator import Paginator


class CommentManagement():

    def list(self, event_id, limit=10, page=1):
        # Check if event_id exists
        if utils.get_object_or_none(Event, id=event_id) is None:
            return None

        comments = Comment.objects.filter(event_id=event_id)
        total = comments.count()
        paginator = Paginator(comments, limit)

        list_of_comments = []
        try:
            for comment in paginator.page(page):
                user = utils.get_object_or_none(User, id=comment.user_id)
                list_of_comments.append({
                    'user_id': comment.user_id,
                    'comment': comment.comment,
                    'id': comment.id,
                    'fullname': user.fullname,
                })
        except:
            pass

        response = {}
        response['total'] = total
        response['list_of_comments'] = list_of_comments

        return response

    def create(self, event_id, user_id, comment):
        # Check if event_id exists
        if utils.get_object_or_none(Event, id=event_id) is None:
            return None

        comment = Comment.objects.create(user_id=user_id, event_id=event_id, comment=comment)

        return comment
