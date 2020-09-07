from django.db import models

from datetime import datetime


class User(models.Model):

    id = models.AutoField(primary_key=True)
    username = models.CharField()
    fullname = models.CharField()
    hashed_password = models.CharField()
    salt = models.CharField()
    verify_code = models.CharField()
    created_at = models.IntegerField()
    is_admin = models.IntegerField()
    
    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'fullname': self.fullname,
            'created_at': datetime.fromtimestamp(self.created_at),
            'is_admin': self.is_admin,
        }

    class Meta:
        db_table = "user_tab"
        app_label = 'entry_task'
