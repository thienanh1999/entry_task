from commonlib.models import Event, Category, EventCategory, Like, Comment, Participant
from . import utils
from django.forms.models import model_to_dict


class EventManagement():

    def list(self, title=None, start=None, end=None, location=None):
        pass

    def retrieve(self, event_id):
        event = utils.get_object_or_none(Event, id=event_id)

        return event

    def update(self, event_id, user_id, **kwargs):
        event = Event.objects.filter(id=event_id)

        if event.count() == 0:
            return None
        else:
            event.update(**kwargs)
            response = model_to_dict(event.first())

            # Update category
            event_category = EventCategory.objects.filter(event_id=event_id)
            response['category'] = []
            for item in event_category:
                category = Category.objects.get(id=item.category_id)
                response['category'].append(model_to_dict(category))

            # Update like
            total = Like.objects.filter(event_id=event_id, user_id=user_id).count()
            response['like'] = total

            # Update Comment
            total = Comment.objects.filter(event_id=event_id, user_id=user_id).count()
            response['comment'] = total

            # Update participant
            total = Participant.objects.filter(event_id=event_id, user_id=user_id).count()
            response['participant'] = total

            return response

    def create(self, data):
        # Check Category
        categories = data['category']
        list_of_category_names = []
        for category in categories:
            obj = utils.get_object_or_none(Category, id=category)
            if obj is None:
                return None
            else:
                list_of_category_names.append(model_to_dict(obj))

        description = data.get('description', None)
        images = data.get('images', None)

        # Create Event
        event = Event(title=data['title'],
                      description=description,
                      start=data['start'],
                      end=data['end'],
                      location=data['location'],
                      images=images)
        event.save()

        # Apply category to event
        response = event.as_dict()
        for category in categories:
            EventCategory.objects.create(event_id=event.id, category_id=category)
        response['category'] = list_of_category_names

        return response
