from django.db import models


class Comment(models.Model):

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(
        null=False
    )
    event_id = models.IntegerField(
        null=False
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment_tab'
        app_label = 'entry_task'
        indexes = [
            models.Index(fields=['event_id'], name='idx_event_id')
        ]
