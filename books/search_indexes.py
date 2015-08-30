from haystack import indexes
from books.models import Book, Series


class BookIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.NgramField(document=True, use_template=True)
    library = indexes.IntegerField(model_attr="library_id")

    def get_model(self):
        return Book

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def get_updated_field(self):
        return 'modified'


class SeriesIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.NgramField(document=True, use_template=True)
    library = indexes.IntegerField(model_attr="library_id")

    def get_model(self):
        return Series

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def get_updated_field(self):
        return 'modified'