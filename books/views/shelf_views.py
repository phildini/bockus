from datetime import timedelta
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import (
    get_object_or_404,
    redirect,
)
from django.utils import timezone
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
    BookOnShelf,
    Shelf,
)
from books.views import (
    SEARCH_UPDATE_MESSAGE,
    LibraryMixin,
)
from readers.models import Reader

class ShelfListView(LibraryMixin, ListView):

    model = Shelf
    template_name = "shelf_list.html"


class ShelfView(LibraryMixin, DetailView):

    model = Shelf
    template_name = "shelf.html"

    def get_context_data(self, **kwargs):
        context = super(ShelfView, self).get_context_data(**kwargs)
        context['books'] = [
            book_on_shelf.book for book_on_shelf in BookOnShelf.objects.filter(
                shelf=self.get_object()
            )
        ]
        return context

class CreateShelfView(LibraryMixin, CreateView):

    model = Shelf
    template_name = "shelf_edit.html"
    fields = ['name',]

    def get_success_url(self):
        return reverse('shelf-list')

    def get_context_data(self, **kwargs):
        context = super(CreateShelfView, self).get_context_data(**kwargs)
        context['action'] = reverse('shelf-create')

        return context

class EditShelfView(LibraryMixin, UpdateView):

    model = Shelf
    template_name = "shelf_edit.html"
    fields = ['name',]

    def get_success_url(self):
        return reverse(
            'shelf-detail',
            kwargs={'pk': self.object.id}
        )

    def get_context_data(self, **kwargs):
        context = super(EditShelfView, self).get_context_data(**kwargs)
        context['action'] = reverse(
            'shelf-edit',
            kwargs={'pk': self.object.id},
        )

        return context

    def form_valid(self, form):
        messages.success(self.request, "{} updated. {}".format(
            self.object, SEARCH_UPDATE_MESSAGE
        ))

        return super(EditShelfView, self).form_valid(form)


class DeleteShelfView(LibraryMixin, DeleteView):

    model = Shelf
    template_name = "shelf_delete.html"

    def get_success_url(self):
        return reverse('shelf-list')

    def form_valid(self, form):
        messages.success(self.request, "{} deleted. {}".format(
            self.object, SEARCH_UPDATE_MESSAGE
        ))

        return super(DeleteShelfView, self).form_valid(form)


class LastWeekShelfView(LibraryMixin, ListView):

    model = Book
    template_name = "shelf.html"
    paginate_by = 25
    paginate_orphans = 5

    def get_queryset(self):
        queryset = super(LastWeekShelfView, self).get_queryset()
        last_week = timezone.now() - timedelta(days=7)
        return queryset.filter(created__gt=last_week)

    def get_context_data(self, **kwargs):
        context = super(LastWeekShelfView, self).get_context_data(**kwargs)
        context['shelf_name'] = 'Added in Last Week'
        context['books'] = context['object_list']
        return context


class LastMonthShelfView(LibraryMixin, ListView):

    model = Book
    template_name = "shelf.html"
    paginate_by = 25
    paginate_orphans = 5

    def get_queryset(self):
        queryset = super(LastMonthShelfView, self).get_queryset()
        last_month = timezone.now() - timedelta(days=30)
        return queryset.filter(created__gt=last_month)

    def get_context_data(self, **kwargs):
        context = super(LastMonthShelfView, self).get_context_data(**kwargs)
        context['shelf_name'] = 'Added in Last Month'
        context['books'] = context['object_list']
        return context