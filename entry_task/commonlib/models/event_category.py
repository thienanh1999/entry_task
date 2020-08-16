from django.db import models


class EventCategory(models.Model):

    id = models.AutoField(primary_key=True)
    event_id = models.IntegerField()
    category_id = models.IntegerField()

    class Meta:
        db_table = 'event_category_tab'
        app_label = 'entry_task'
