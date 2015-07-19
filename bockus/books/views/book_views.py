import dropbox

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
    ListView,
    UpdateView,
    View,
)

from allauth.socialaccount.models import SocialApp, SocialToken

from books.models import (
    Book,
    BookFileVersion,
)

from books.utils import parse_folder

from readers.models import Reader

from libraries.models import Library, Librarian

SEARCH_UPDATE_MESSAGE = "Changes may not show in search immediately."


class LibraryMixin(object):

    def get_queryset(self):
        queryset = super(LibraryMixin, self).get_queryset()
        queryset = queryset.filter(
            library__librarian__user=self.request.user
        )
        return queryset

    def form_valid(self, form):
        response = super(LibraryMixin, self).form_valid(form)

        self.object.library = Librarian.objects.get(
            user=self.request.user
        ).library
        self.object.save()

        return response


class BookListView(LibraryMixin, ListView):

    model = Book
    template_name = "book_list.html"

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
        context['readers'] = Reader.objects.filter(user=self.request.user)

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
        book_file_version = BookFileVersion.objects.filter(
            book=book,
        )[0]
        book_file_path = book_file_version.path
        try:
            dropbox_app_creds = SocialApp.objects.filter(
                provider='dropbox_oauth2'
            )[0]
            token = SocialToken.objects.get(
                account__user=request.user,
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
            from_email="books@inkpebble.com",
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


class ImportBooksView(View):

    def get(self, request, *args, **kwargs):
        try:
            token = SocialToken.objects.get(
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
        client = dropbox.client.DropboxClient(token)

        try:
            library = Library.objects.get(librarian__user=request.user)
        except Library.DoesNotExist:
            library = Library.objects.create(
                title="{}'s Library".format(request.user),
            )
            Librarian.objects.create(
                user=request.user,
                library=library,
            )

        parse_folder(
            client=client,
            path='/eBooks/sortme/McCaffrey, Anne',
            library=library,
        )

        return redirect('book-list')
