from django.db import models


class EventCategory(models.Model):

    id = models.AutoField(primary_key=True)
    event_id = models.IntegerField(
        null=False
    )
    category_id = models.IntegerField(
        null=False
    )

    class Meta:
        db_table = 'event_category_tab'
        app_label = 'entry_task'
        indexes = [
            models.Index(fields=['event_id'], name='idx_event_id')
        ]
        unique_together = [
            ['category_id', 'event_id']
        ]
