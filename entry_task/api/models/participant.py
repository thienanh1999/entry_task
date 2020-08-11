from django.db import models


class Participant(models.Model):

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(
        null=False
    )
    event_id = models.IntegerField(
        null=False
    )

    class Meta:
        db_table = 'participant_tab'
        app_label = 'entry_task'
        unique_together = [
            ['user_id', 'event_id'],
            ['event_id', 'user_id'],
        ]
