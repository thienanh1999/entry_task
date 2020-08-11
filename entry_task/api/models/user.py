from django.db import models


class User(models.Model):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    hashed_password = models.CharField(
        max_length=255,
        default=''
    )
    hash_key = models.CharField(
        max_length=255,
        default='kEy'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = "user_tab"
        app_label = 'entry_task'
        unique_together = [
            ['username']
        ]
