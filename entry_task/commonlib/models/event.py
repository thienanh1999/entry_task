from django.db import models

from datetime import datetime


class Event(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField()
    description = models.TextField()
    created_at = models.IntegerField()
    start = models.IntegerField()
    end = models.IntegerField()
    location = models.CharField()
    images = models.TextField()

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start': datetime.fromtimestamp(self.start),
            'end': datetime.fromtimestamp(self.end),
            'location': self.location,
            'images': self.images,
            'created_at': datetime.fromtimestamp(self.created_at),
        }

    class Meta:
        db_table = "event_tab"
        app_label = 'entry_task'
