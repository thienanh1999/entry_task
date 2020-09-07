from django.db import models


class Like(models.Model):

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(
        null=False
    )
    event_id = models.IntegerField(
        null=False
    )
    is_deleted = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'like_tab'
        app_label = 'entry_task'
        unique_together = [
            ['event_id', 'user_id'],
            ['user_id', 'event_id'],
        ]
