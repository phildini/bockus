import dropbox

from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
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

from allauth.socialaccount.models import SocialApp, SocialToken

from .models import (
    Book,
    BookFileVersion,
)


class BookListView(ListView):

    model = Book
    template_name = "book_list.html"


class BookView(DetailView):

    model = Book
    template_name = "book.html"


class CreateBookView(CreateView):

    model = Book
    template_name = "add_or_edit_book.html"
    fields = ['title',]

    def get_success_url(self):
        return reverse('book-list')


class EditBookView(UpdateView):

    model = Book
    template_name = "add_or_edit_book.html"
    fields = ['title',]

    def get_success_url(self):
        return reverse('book-detail', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super(EditBookView, self).get_context_data(**kwargs)
        context['action'] = reverse(
            'book-edit',
            kwargs={'pk': self.get_object().id},
        )

        return context


class DeleteBookView(DeleteView):

    model = Book
    template_name = "book_delete.html"

    def get_success_url(self):
        return reverse('book-list')


class SendBookView(View):

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book.objects, pk=kwargs.get('pk'))
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
            raise Http404()
        client = dropbox.client.DropboxClient(token)

        message = EmailMessage(
            subject='A book for you!',
            body=book.title,
            from_email="books@inkpebble.com",
            to=['pjj@philipjohnjames.com'],
        )
        f, metadata = client.get_file_and_metadata(book_file_path)
        message.attach(
            'book.{}'.format(book_file_version.filetype),
            f.read(),
            metadata.get('mime_type'),
        )
        message.send()
        return redirect(book)