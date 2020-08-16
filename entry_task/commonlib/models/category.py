from django.db import models


class Category(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField()

    class Meta:
        db_table = 'category_tab'
        app_label = 'entry_task'
