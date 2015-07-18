from haystack import indexes
from books.models import Book, Series


class BookIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    library = indexes.IntegerField(model_attr="library_id")

    def get_model(self):
        return Book

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class SeriesIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Series

    def index_queryset(self, using=None):
        return self.get_model().objects.all()