import dropbox
import json

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404
from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
    redirect,
)
from django import forms
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from allauth.socialaccount.models import SocialToken

from books.forms import ImportForm

from books.models import (
    Book,
    BookFileVersion,
    BookEmail,
    BookOnShelf,
    Series,
    Shelf,
)

from readers.models import Reader

from libraries.models import Library, Librarian, LibraryImport

SEARCH_UPDATE_MESSAGE = "Changes may not show in search immediately."


class LibraryMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(
                '{}?next={}'.format(settings.LOGIN_URL, request.path)
            )

        return super(LibraryMixin, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(LibraryMixin, self).get_queryset()
        queryset = queryset.filter(
            library__librarian__user=self.request.user
        )
        return queryset

    def get_object(self, queryset=None):
        instance = super(LibraryMixin, self).get_object(queryset)

        if not instance.library.librarian_set.filter(user=self.request.user):
            raise PermissionDenied

        return instance

    def form_valid(self, form):
        form.instance.library = Librarian.objects.get(
            user=self.request.user
        ).library
        response = super(LibraryMixin, self).form_valid(form)

        return response


class BookListView(LibraryMixin, ListView):

    model = Book
    template_name = "book_list.html"
    paginate_by = 25
    paginate_orphans = 5

    def get_queryset(self):
        queryset = super(BookListView, self).get_queryset()
        return queryset.order_by(
            'author',
            'series',
            'number_in_series',
        )

    def get_success_url(self):
        return reverse('book-list')

    def get_form_kwargs(self):
        """
        Right now, using this only for POST, PUT
        """
        kwargs = {}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form(self, form_class=None):
        form = forms.Form(**self.get_form_kwargs())
        queryset = self.get_queryset()
        page_size = self.get_paginate_by(queryset)
        page_num = 1
        if self.request.GET.get('page'):
            page_num = int(self.request.GET.get('page'))
        else:
            page_num = int(form.data.get('page', 1))
        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
        choices = [(book.id, book.title) for book in paginator.page(page_num)]
        actions = [
            ('shelve', 'Add to shelf...'),
            ('merge', 'Merge Selected'),
            ('delete', 'Delete Selected'),
        ]
        form.fields['books'] = forms.MultipleChoiceField(
            required=False,
            choices=choices,
            widget=forms.CheckboxSelectMultiple()
        )
        form.fields['actions'] = forms.ChoiceField(
            required=False,
            choices=actions,
        )
        form.fields['page'] = forms.IntegerField(
            required=False,
            widget=forms.HiddenInput()
        )
        return form

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if form.cleaned_data.get('actions'):
            if form.cleaned_data.get('books'):
                books = [int(book) for book in form.cleaned_data.get('books')]
                self.request.session['selected_books'] = json.dumps(books)
                if form.cleaned_data.get('actions') == 'merge':
                    return redirect(reverse('books-merge'))
                if form.cleaned_data.get('actions') == 'shelve':
                    return redirect(reverse('books-shelve'))
                if form.cleaned_data.get('actions') == 'delete':
                    return redirect(reverse('books-delete'))
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.add_message(
            self.request,
            messages.ERROR,
            'Something went wrong. Try again.',
        )
        return redirect(reverse('book-list'))

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['running_imports'] = LibraryImport.objects.filter(
            librarian__user=self.request.user,
            status__in=(LibraryImport.PENDING, LibraryImport.PROCESSING),
        )
        context['form'] = self.get_form()
        return context


class BookView(LibraryMixin, FormView):

    model = Book
    template_name = "book.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Book.objects, pk=kwargs.get('pk'))
        return super(BookView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BookView, self).get_context_data(**kwargs)
        context['book'] = self.object
        context['can_send_to_kindle'] = BookFileVersion.objects.filter(
            book=self.object,
            filetype__in=(BookFileVersion.MOBI, BookFileVersion.PDF),
        )
        context['can_send_to_other'] = BookFileVersion.objects.filter(
            book=self.object,
            filetype__in=(BookFileVersion.EPUB, BookFileVersion.PDF),
        )
        context['kindles'] = Reader.objects.filter(
            user=self.request.user,
            kind=Reader.KINDLE,
        )
        context['other_readers'] = Reader.objects.filter(
            user=self.request.user,
            kind=Reader.IBOOKS,
        )
        context['form'] = self.get_form()
        return context

    def get_form_kwargs(self):
        """
        Right now, using this only for POST, PUT
        """
        kwargs = {}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form(self, form_class=None):
        form = forms.Form(**self.get_form_kwargs())
        shelves = [
            (shelf.id, shelf.name) for shelf in Shelf.objects.filter(
                library__librarian__user=self.request.user
            )
        ]
        form.fields['shelf'] = forms.ChoiceField(
            choices=shelves,
            required=False,
            label="Add to shelf:",
        )
        return form

    def get_success_url(self):
        return reverse('book-detail', args=[self.object.pk])

    def form_valid(self, form):
        shelf = get_object_or_404(Shelf.objects, pk=form.cleaned_data.get('shelf'))
        BookOnShelf.objects.create(shelf=shelf, book=self.object)
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Added to <a href="{}">shelf</a>'.format(shelf.get_absolute_url()),
            extra_tags='safe',
        )
        return redirect(self.get_success_url())


class CreateBookView(LibraryMixin, CreateView):

    model = Book
    template_name = "book_edit.html"
    fields = ['title', 'author', 'series', 'number_in_series']

    def get_success_url(self):
        return reverse('book-list')


class EditBookView(LibraryMixin, UpdateView):

    model = Book
    template_name = "book_edit.html"
    fields = ['title', 'author', 'series', 'number_in_series']

    def get_success_url(self):
        return reverse('book-detail', args=[self.object.pk])

    def get_form(self, form_class):
        form = super(EditBookView, self).get_form(form_class)
        form.fields['series'].queryset = Series.objects.filter(
            library__librarian__user=self.request.user,
        )
        return form

    def get_context_data(self, **kwargs):
        context = super(EditBookView, self).get_context_data(**kwargs)
        context['action'] = reverse(
            'book-edit',
            kwargs={'pk': self.get_object().id},
        )

        return context

    def form_valid(self, form):
        response = super(EditBookView, self).form_valid(form)
        if (
            not form.cleaned_data.get('author') and
            form.cleaned_data.get('series') and
            form.cleaned_data.get('series').author
        ):
            self.object.author = form.cleaned_data.get('series').author
            self.object.save()

        messages.success(self.request, "{} updated. {}".format(
            self.object, SEARCH_UPDATE_MESSAGE
        ))

        return response


class DeleteBookView(LibraryMixin, DeleteView):

    model = Book
    template_name = "book_delete.html"

    def get_success_url(self):
        return reverse('book-list')

    def form_valid(self, form):
        messages.success(self.request, "{} deleted. {}".format(
            self.object, SEARCH_UPDATE_MESSAGE
        ))

        return super(DeleteBookView, self).form_valid(form)


class MergeBookView(TemplateView):

    template_name = "books_merge.html"

    def post(self, request, *args, **kwargs):
        selected_books = json.loads(self.request.session.get('selected_books'))
        try:
            books = Book.objects.filter(
                pk__in=selected_books,
                library__librarian__user=self.request.user,
            ).order_by('-modified')
        except:
            raise Http404()
        new_book = books[0]
        meta_json = new_book.meta
        if meta_json:
            meta = json.loads(meta)
            merged_books = meta.get('merged', [])
        else:
            meta = {}
            merged_books = []
        for book in books[1:]:
            for version in BookFileVersion.objects.filter(book=book):
                version.book = new_book
                version.save()
            merged_books.append(book.to_dict()),
            book.delete()
        meta['merged'] = merged_books
        new_book.meta = json.dumps(meta)
        new_book.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Successfully merged books!",
        )
        return redirect(reverse('book-detail', args=[new_book.pk]))


    def get_context_data(self, **kwargs):
        context = super(MergeBookView, self).get_context_data(**kwargs)
        selected_books = json.loads(self.request.session.get('selected_books'))
        context['books'] = get_list_or_404(
            Book.objects,
            pk__in=selected_books,
            library__librarian__user=self.request.user,
        )
        return context


class ShelveBooksView(FormView):

    template_name = "shelve_books.html"

    def get_context_data(self, **kwargs):
        context = super(ShelveBooksView, self).get_context_data(**kwargs)
        selected_books = json.loads(self.request.session.get('selected_books'))
        context['books'] = get_list_or_404(
            Book.objects,
            pk__in=selected_books,
            library__librarian__user=self.request.user,
        )
        return context

    def get_form_kwargs(self):
        """
        Right now, using this only for POST, PUT
        """
        kwargs = {}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form(self, form_class=None):
        form = forms.Form(**self.get_form_kwargs())
        shelves = [
            (shelf.id, shelf.name) for shelf in Shelf.objects.filter(
                library__librarian__user=self.request.user
            )
        ]
        form.fields['shelf'] = forms.ChoiceField(
            choices=shelves,
            required=True,
        )
        return form

    def get_success_url(self):
        return reverse('book-list')

    def form_valid(self, form):
        shelf = get_object_or_404(Shelf.objects, pk=form.cleaned_data.get('shelf'))
        books = get_list_or_404(
            Book.objects,
            pk__in=json.loads(self.request.session.get('selected_books')),
            library__librarian__user=self.request.user,
        )
        for book in books:
            BookOnShelf.objects.create(shelf=shelf, book=book)
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Added books to shelf"
        )
        return redirect(reverse('shelf-detail', kwargs={'pk':shelf.id}))


class DeleteBooksView(TemplateView):

    template_name = "books_delete.html"

    def post(self, request, *args, **kwargs):
        selected_books = json.loads(self.request.session.get('selected_books'))
        try:
            books = Book.objects.filter(
                pk__in=selected_books,
                library__librarian__user=self.request.user,
            ).order_by('-modified')
        except:
            raise Http404()
        books.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            "Successfully deleted books",
        )
        return redirect(reverse('book-list'))

    def get_context_data(self, **kwargs):
        context = super(DeleteBooksView, self).get_context_data(**kwargs)
        selected_books = json.loads(self.request.session.get('selected_books'))
        context['books'] = get_list_or_404(
            Book.objects,
            pk__in=selected_books,
            library__librarian__user=self.request.user,
        )
        return context


class SendBookView(View):

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(
            Book.objects,
            pk=kwargs.get('pk'),
            library=Librarian.objects.get(user=self.request.user).library,
        )
        reader = get_object_or_404(Reader.objects, pk=kwargs.get('reader'))
        if reader.kind == Reader.KINDLE:
            book_file_version = book.get_version_for_kindle()
        else:
            book_file_version = book.get_version_for_other()
        if book_file_version:
            BookEmail.objects.create(
                book_file=book_file_version,
                reader=reader,
            )
            messages.add_message(
                request,
                messages.SUCCESS,
                "Book is on its way!",
            )

            return redirect(book)

        messages.add_message(
            request,
            messages.ERROR,
            'Something went wrong. Try sending again.',
        )
        return redirect(book)


class ImportBooksView(FormView):

    form_class = ImportForm
    template_name = "import.html"

    def dispatch(self, request, *args, **kwargs):

        try:
            self.token = SocialToken.objects.get(
                account__user=request.user,
                app__provider='dropbox_oauth2',
            ).token
        except:
            messages.add_message(
                request,
                messages.ERROR,
                'You need to connect to Dropbox before importing.',
            )
            return redirect(reverse('socialaccount_connections'))
        self.client = dropbox.client.DropboxClient(self.token)

        return super(ImportBooksView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('book-list')

    def get_context_data(self, **kwargs):
        context = super(ImportBooksView, self).get_context_data(**kwargs)
        context['action'] = reverse('books-import')

        return context

    def get_form_kwargs(self):
        kwargs = super(ImportBooksView, self).get_form_kwargs()
        kwargs['token'] = self.token
        kwargs['client'] = self.client
        return kwargs

    def form_valid(self, form):
        try:
            librarian = Librarian.objects.get(user=self.request.user)
        except Librarian.DoesNotExist:
            library = Library.objects.create(
                title="{}'s Library".format(self.request.user),
            )
            librarian = Librarian.objects.create(
                user=self.request.user,
                library=library,
            )

        if 'select_all_option' in form.cleaned_data.get('folders'):
            LibraryImport.objects.create(
                librarian=librarian,
                path='/',
            )

        else:
            for folder in form.cleaned_data.get('folders'):
                LibraryImport.objects.create(
                    librarian=librarian,
                    path=folder,
                )
        messages.add_message(
            self.request,
            messages.INFO,
            "We've started importing your books. Hooray! You'll receive an email when we're all done.",
        )
        return super(ImportBooksView, self).form_valid(form)
