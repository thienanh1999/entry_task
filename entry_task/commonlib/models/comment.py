from django.db import models

from datetime import datetime


class Comment(models.Model):

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    event_id = models.IntegerField()
    comment = models.TextField()
    created_at = models.IntegerField()
    
    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_id': self.event_id,
            'comment': self.comment,
            'created_at': datetime.fromtimestamp(self.created_at)
        }

    class Meta:
        db_table = 'comment_tab'
        app_label = 'entry_task'
