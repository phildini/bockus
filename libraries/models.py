from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField
from model_utils.models import TimeStampedModel


class Library(TimeStampedModel):

    title = models.CharField(max_length=255)
    allowed_users = models.IntegerField(default=5)
    meta = JSONField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'libraries'


class Librarian(TimeStampedModel):

    user = models.ForeignKey(User)
    library = models.ForeignKey('Library')

    def __str__(self):
        return "{} is a librarian of {}".format(
            self.user,
            self.library,
        )


class LibraryImport(TimeStampedModel):
    PENDING = 'pending'
    PROCESSING = 'processing'
    DONE = 'done'
    ERROR = 'error'

    DROPBOX = 'dropbox'

    STATUSES = (
        (PENDING, 'pending'),
        (PROCESSING, 'processing'),
        (DONE, 'done'),
        (ERROR, 'error'),
    )

    SOURCES = (
        (DROPBOX, 'dropbox'),
    )

    librarian = models.ForeignKey('Librarian')
    source = models.CharField(
        max_length=20,
        choices=SOURCES,
        default=DROPBOX,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUSES,
        default=PENDING,
    )
    path = models.TextField()

    def __str__(self):
        return "{}: from {} into {}".format(
            self.status,
            self.source,
            self.librarian.library,
        )


