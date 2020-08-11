from django.db import models
import datetime


class Event(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=255,
        null=False,
    )
    description = models.TextField(
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    start = models.DateTimeField(
        null=False,
    )
    end = models.DateTimeField(
        null=False,
    )
    location = models.CharField(
        max_length=255,
        null=False,
        default='65 Le Loi',
    )
    images = models.TextField(
        null=True,
    )

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start': self.start,
            'end': self.end,
            'location': self.location,
            'images': self.images,
            'created_at': self.created_at,
        }

    class Meta:
        db_table = "event_tab"
        app_label = 'entry_task'
        indexes = [
            models.Index(fields=['location'], name='idx_location'),
            models.Index(fields=['end', 'start'], name='idx_end_start'),
            models.Index(fields=['title', 'location'], name='idx_title_location'),
        ]
