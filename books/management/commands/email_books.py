import dropbox
import json
import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage

from allauth.socialaccount.models import SocialApp, SocialToken

from books.forms import ImportForm

from books.models import (
    Book,
    BookFileVersion,
    BookEmail,
    Series,
)

from readers.models import Reader

from libraries.models import Library, Librarian

logger = logging.getLogger('scripts')


class Command(BaseCommand):
    help = "send pending book emails"

    def handle(self, *args, **options):
        logger.debug('Starting book email send cronjob')
        books_to_send = BookEmail.objects.filter(
            status=BookEmail.PENDING)[:4]
        for book_email in books_to_send:
            logger.debug('Working on email job %s' % book_email.id)
            book_email.status = BookEmail.PROCESSING
            book_email.save()
            book_file_path = book_email.book_file.path
            token = None
            try:
                dropbox_app_creds = SocialApp.objects.filter(
                    provider='dropbox_oauth2'
                )[0]
                token = SocialToken.objects.get(
                    account__user=book_email.book_file.book.added_by,
                    app__provider='dropbox_oauth2'
                ).token
            except:
                logger.exception(
                    'Error getting dropbox token for email job %s' % book_email.id
                )
                book_email.status = BookEmail.ERROR
                book_email.save()
            if token:
                client = dropbox.client.DropboxClient(token)

                message = EmailMessage(
                    subject='[Booksonas] A book for you!',
                    body=book_email.book_file.book.title,
                    from_email="books@booksonas.com",
                    to=[book_email.reader.email,],
                )
                f, metadata = client.get_file_and_metadata(book_file_path)
                message.attach(
                    'book.{}'.format(book_email.book_file.filetype),
                    f.read(),
                    metadata.get('mime_type'),
                )
                message.send()
                book_email.status=BookEmail.SENT
                book_email.save()
                logger.debug('Successfully sent %s' % book_email.id)
        logger.debug('Book email cronjob finished')
