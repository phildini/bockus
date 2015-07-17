from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField
from model_utils.models import TimeStampedModel


class Trove(TimeStampedModel):

    title = models.CharField(max_length=255)
    allowed_users = models.IntegerField(default=5)
    meta = JSONField(blank=True)

    def __str__(self):
        return self.title


class TroveLibrarian(TimeStampedModel):

    user = models.ForeignKey(User)
    trove = models.ForeignKey('Trove')

    def __str__(self):
        return "{} is a librarian of {}".format(
            self.user,
            self.trove,
        )

