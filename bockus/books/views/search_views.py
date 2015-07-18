from django.http import Http404
from haystack.generic_views import SearchView
from libraries.models import Library


class LibrarySearchView(SearchView):
    """ Searches across whole Library

    Restricts search to books and series in one Library.
    """

    def get_queryset(self):
        queryset = super(LibrarySearchView, self).get_queryset()
        try:
            library = Library.objects.get(librarian__user=self.request.user)
        except Library.DoesNotExist:
            raise Http404()
        return queryset.filter(library=library.id)

