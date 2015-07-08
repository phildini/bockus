from django.core.mail import send_mail
from django.shortcuts import (
    get_object_or_404,
    redirect,
)
from django.views.generic import View, ListView, DetailView
from .models import Book


class BookListView(ListView):

    model = Book
    template_name = "book_list.html"


class BookView(DetailView):

    model = Book
    template_name = "book.html"

class SendBookView(View):
    
    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book.objects, pk=kwargs.get('pk'))
        message = "{}".format(book.title)
        send_mail(
            subject='A book for you!',
            message=message,
            from_email="books@inkpebble.com",
            recipient_list=['pjj@philipjohnjames.com'],
        )
        return redirect(book)