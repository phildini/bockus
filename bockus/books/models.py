from django.db import models
from django.utils.timezone import now
from jsonfield import JSONField
from model_utils.models import TimeStampedModel
from troves.models import Trove

class Book(TimeStampedModel):

    title = models.CharField(max_length=255)
    meta = JSONField()

    def __str__(self):
        return self.title


class BookFileVersion(TimeStampedModel):
    DROPBOX = 'dropbox'
    STORAGE_PROVIDERS = (
        ('dropbox', 'dropbox'),
    )

    EPUB = 'epub'
    PDF = 'pdf'
    MOBI = 'mobi'
    FILETYPES = (
        ('epub', 'epub'),
        ('pdf', 'pdf'),
        ('mobi', 'mobi'),
    )

    book = models.ForeignKey('Book')
    filetype = models.CharField(max_length=10, choices=FILETYPES)
    storage_provider = models.CharField(
        max_length=10,
        choices=STORAGE_PROVIDERS,
        default=DROPBOX,
    )
    path = models.CharField(max_length=255, null=True)
    meta = JSONField()

    def __str__(self):
        return "{} - {}".format(self.book.title, self.filetype)




