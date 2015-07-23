import dropbox

from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import (
    get_object_or_404,
    redirect,
)
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
    View,
)

from allauth.socialaccount.models import SocialApp, SocialToken

from books.forms import ImportForm

from books.models import (
    Book,
    BookFileVersion,
    Series,
)

from books.utils import (
    parse_folder,
    parse_multiple_folders,
)

from readers.models import Reader

from libraries.models import Library, Librarian

SEARCH_UPDATE_MESSAGE = "Changes may not show in search immediately."


class LibraryMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
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

class BookView(LibraryMixin, DetailView):

    model = Book
    template_name = "book.html"

    def get_context_data(self, **kwargs):
        context = super(BookView, self).get_context_data(**kwargs)
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
        return context


class CreateBookView(LibraryMixin, CreateView):

    model = Book
    template_name = "add_or_edit_book.html"
    fields = ['title', 'author', 'series', 'number_in_series']

    def get_success_url(self):
        return reverse('book-list')


class EditBookView(LibraryMixin, UpdateView):

    model = Book
    template_name = "add_or_edit_book.html"
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
            book_file_path = book_file_version.path
            try:
                dropbox_app_creds = SocialApp.objects.filter(
                    provider='dropbox_oauth2'
                )[0]
                token = SocialToken.objects.get(
                    account__user=book.added_by,
                    app__provider='dropbox_oauth2'
                ).token
            except:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Couldn't make connection to Dropbox",
                )
                return redirect(book)

            client = dropbox.client.DropboxClient(token)

            message = EmailMessage(
                subject='A book for you!',
                body=book.title,
                from_email="books@booksonas.com",
                to=[reader.email,],
            )
            f, metadata = client.get_file_and_metadata(book_file_path)
            message.attach(
                'book.{}'.format(book_file_version.filetype),
                f.read(),
                metadata.get('mime_type'),
            )
            message.send()
            messages.add_message(request, messages.SUCCESS, 'Book emailed!')
            return redirect(book)

        messages.add_message(
            request,
            messages.INFO,
            'Something went wrong. Try sending again',
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
            library = Library.objects.get(
                librarian__user=self.request.user,
            )
        except Library.DoesNotExist:
            library = Library.objects.create(
                title="{}'s Library".format(request.user),
            )
            Librarian.objects.create(
                user=self.request.user,
                library=library,
            )

        if 'select_all_option' in form.cleaned_data.get('folders'):
            parse_folder(
                client=self.client,
                path='/',
                library=library,
                user=self.request.user,
            )
        else:
            parse_multiple_folders(
                client=self.client,
                folders=form.cleaned_data.get('folders'),
                library=library,
                user=self.request.user,
            )
        return super(ImportBooksView, self).form_valid(form)
