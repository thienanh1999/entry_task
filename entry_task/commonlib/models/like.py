from django.db import models


class Like(models.Model):

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    event_id = models.IntegerField()
    is_deleted = models.IntegerField()

    class Meta:
        db_table = 'like_tab'
        app_label = 'entry_task'
