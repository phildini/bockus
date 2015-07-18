from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404
from django.shortcuts import (
    get_object_or_404,
    redirect,
)
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from books.models import (
    Book,
    Series,
)

from books.views import (
    SEARCH_UPDATE_MESSAGE,
    LibraryMixin,
)

from readers.models import Reader


class SeriesListView(LibraryMixin, ListView):

    model = Series
    template_name = "series_list.html"


class SeriesView(LibraryMixin, DetailView):

    model = Series
    template_name = "series.html"

    def get_context_data(self, **kwargs):
        context = super(SeriesView, self).get_context_data(**kwargs)
        context['books'] = Book.objects.filter(
            series=self.get_object(),
        ).order_by(
            'number_in_series',
        )
        context['readers'] = Reader.objects.filter(user=self.request.user)
        return context

class CreateSeriesView(LibraryMixin, CreateView):

    model = Series
    template_name = "add_or_edit_series.html"
    fields = ['name', 'author']

    def get_success_url(self):
        return reverse('series-list')

    def get_context_data(self, **kwargs):
        context = super(CreateSeriesView, self).get_context_data(**kwargs)
        context['action'] = reverse('series-create')

        return context


class EditSeriesView(LibraryMixin, UpdateView):

    model = Series
    template_name = "add_or_edit_series.html"
    fields = ['name', 'author']

    def get_success_url(self):
        return reverse(
            'series-detail',
            kwargs={'pk': self.object.id}
        )

    def get_context_data(self, **kwargs):
        context = super(EditSeriesView, self).get_context_data(**kwargs)
        context['action'] = reverse(
            'series-edit',
            kwargs={'pk': self.object.id},
        )

        return context

    def form_valid(self, form):
        messages.success(self.request, "{} updated. {}".format(
            self.object, SEARCH_UPDATE_MESSAGE
        ))

        return super(EditSeriesView, self).form_valid(form)


class DeleteSeriesView(LibraryMixin, DeleteView):

    model = Series
    template_name = "series_delete.html"

    def get_success_url(self):
        return reverse('series-list')

    def form_valid(self, form):
        messages.success(self.request, "{} deleted. {}".format(
            self.object, SEARCH_UPDATE_MESSAGE
        ))

        return super(DeleteSeriesView, self).form_valid(form)

