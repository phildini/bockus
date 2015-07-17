from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import now
from jsonfield import JSONField
from model_utils.models import TimeStampedModel
from troves.models import Trove

class Book(TimeStampedModel):

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)
    series = models.ForeignKey('Series', null=True, blank=True)
    number_in_series = models.IntegerField(null=True, blank=True)
    meta = JSONField()

    def __str__(self):
        string = self.title
        if self.author:
            string = "{} by {}".format(string, self.author)
        if self.series:
            if self.number_in_series:
                string = "{} ({} {})".format(
                    string,
                    self.series.name,
                    self.number_in_series,
                )
            else:
                string = "{} ({})".format(string, self.series.name)
        return string

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.id})

    @property
    def is_book(self):
        return True


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


class Series(TimeStampedModel):

    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "{} by {}".format(self.name, self.author)

    def get_absolute_url(self):
        return reverse('series-detail', kwargs={'pk': self.id})

    @property
    def is_series(self):
        return True





