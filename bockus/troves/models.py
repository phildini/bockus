from django.db import models
from jsonfield import JSONField
from model_utils.models import TimeStampedModel



class Trove(TimeStampedModel):

    title = models.CharField(max_length=255)
    meta = JSONField()

    def __str__(self):
        return self.title
