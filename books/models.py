from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import now
from jsonfield import JSONField
from model_utils.models import TimeStampedModel
from libraries.models import Library
from readers.models import Reader


class Book(TimeStampedModel):

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)
    series = models.ForeignKey('Series', null=True, blank=True)
    number_in_series = models.IntegerField(null=True, blank=True)
    library = models.ForeignKey(Library)
    added_by = models.ForeignKey(User)
    meta = JSONField(blank=True)

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

    def to_dict(self):
        blob = {
            'title': self.title,
            'author': self.author,
            'library': self.library.id,
            'added_by': self.added_by.id,
            'meta': self.meta,
        }
        if self.series:
            blob['series'] = self.series.id
        if self.number_in_series:
            blob['number_in_series'] = self.number_in_series
        return blob

    @property
    def is_book(self):
        return True

    @property
    def epub(self):
        if not hasattr(self, '_epub') or not self._epub:
            try:
                self._epub = BookFileVersion.objects.filter(
                    book=self,
                    filetype=BookFileVersion.EPUB,
                )[0]
            except (BookFileVersion.DoesNotExist, IndexError):
                self._epub = None
        return self._epub

    @property
    def pdf(self):
        if not hasattr(self, '_pdf') or not self._pdf:
            try:
                self._pdf = BookFileVersion.objects.filter(
                    book=self,
                    filetype=BookFileVersion.PDF,
                )[0]
            except (BookFileVersion.DoesNotExist, IndexError):
                self._pdf = None
        return self._pdf

    @property
    def mobi(self):
        if not hasattr(self, '_mobi') or not self._mobi:
            try:
                self._mobi = BookFileVersion.objects.filter(
                    book=self,
                    filetype=BookFileVersion.MOBI,
                )[0]
            except (BookFileVersion.DoesNotExist, IndexError):
                self._mobi =  None
        return self._mobi


    def get_version_for_kindle(self):
        if self.mobi:
            return self.mobi
        return self.pdf

    def get_version_for_other(self):
        if self.epub:
            return self.epub
        return self.pdf


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
    path = models.TextField(null=True)
    meta = JSONField()

    def __str__(self):
        return "{} - {}".format(self.book.title, self.filetype)


class BookEmail(TimeStampedModel):
    PENDING = 'pending'
    PROCESSING = 'processing'
    SENT = 'sent'
    ERROR = 'error'
    STATUSES = (
        ('pending', 'pending'),
        ('processing', 'processing'),
        ('sent', 'sent'),
        ('error', 'error'),
    )

    book_file = models.ForeignKey('BookFileVersion')
    reader = models.ForeignKey(Reader)
    status = models.CharField(
        max_length=20,
        choices=STATUSES,
        default=PENDING,
    )

    def __str__(self):
        return "{}: {} to {}".format(
            self.status, self.book_file.id, self.reader,
        )


class Series(TimeStampedModel):

    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)
    library = models.ForeignKey(Library)
    meta = JSONField(blank=True)

    def __str__(self):
        return "{} by {}".format(self.name, self.author)

    def get_absolute_url(self):
        return reverse('series-detail', kwargs={'pk': self.id})

    @property
    def is_series(self):
        return True

    class Meta:
        verbose_name_plural = 'series'


class Shelf(TimeStampedModel):

    name = models.CharField(max_length=255)
    library = models.ForeignKey(Library)
    meta = JSONField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shelf-detail', kwargs={'pk':self.id})

    class Meta:
        verbose_name_plural = 'shelves'


class BookOnShelf(TimeStampedModel):

    book = models.ForeignKey('Book')
    shelf = models.ForeignKey('Shelf')

    def __str__(self):
        return '"{}" on {}'.format(self.book, self.shelf)

    class Meta:
        verbose_name_plural = 'books on shelves'
