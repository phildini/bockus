from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from model_utils.models import TimeStampedModel


class Reader(TimeStampedModel):

    IBOOKS = 'iBooks'
    KINDLE = 'Kindle'
    TYPES = (
        (IBOOKS, 'iBooks (.epub, .pdf)'),
        (KINDLE, 'Kindle (.mobi, .pdf)'),
    )

    name = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User)
    kind = models.CharField(max_length=10, choices=TYPES)
    email = models.EmailField()

    def __str__(self):
        return "{}'s {}".format(self.user, self.kind)

    def get_absolute_url(self):
        return reverse("reader-detail", kwargs={'pk': self.id})
