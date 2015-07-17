import dropbox
import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from books.models import Book, BookFileVersion


class Command(BaseCommand):
    help = "add books from dropbox to the db"

    books = []
    mimetypes = (
        "application/pdf",
        "application/x-mobipocket-ebook",
        "application/epub+zip",
    )

    def handle(self, *args, **options):
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(settings.DROPBOX_APP_KEY,
            settings.DROPBOX_APP_SECRET,
        )
        authorize_url = flow.start()
        print('1. Go to: ' + authorize_url)
        print('2. Click "Allow" (you might have to log in first)')
        print('3. Copy the authorization code.')
        code = input("Enter the authorization code here: ").strip()
        access_token, user_id = flow.finish(code)
        self.client = dropbox.client.DropboxClient(access_token)
        print('linked account: ', self.client.account_info())
        self.parse_folder('/eBooks/sortme/McCaffrey, Anne')

        with open('titles.json', 'w') as outfile:
            json.dump(self.books, outfile, indent=4)

    def parse_folder(self, path):
        print("working on {}".format(path))
        metadata = self.client.metadata(path)
        if not metadata.get('is_dir'):
            self.parse_item(metadata)
        else: 
            for item in metadata.get('contents'):
                if not item.get('is_dir'):
                    self.parse_item(item)
                else:
                    self.parse_folder(item.get('path'))

    def parse_item(self, item):
        if item.get('mime_type') in self.mimetypes:
            filename = item.get('path').split('/')[-1]
            name, extension = os.path.splitext(filename)
            self.books.append(name)
            self.books.append(extension)
            try:
                bookfile = BookFileVersion.objects.get(
                    path=item.get('path'),
                    filetype=extension[1:],
                )
            except BookFileVersion.DoesNotExist:
                try:
                    bookfile = BookFileVersion.objects.get(
                        path=item.get('path'),
                    )
                    new_bookfile = BookFileVersion.objects.create(
                        path=item.get('path'),
                        filetype=extension[1:],
                        book=bookfile.book,
                        storage_provider='dropbox',
                    )
                except BookFileVersion.DoesNotExist:
                    book = Book.objects.create(
                        title=name,
                    )
                    bookfile = BookFileVersion.objects.create(
                        path=item.get('path'),
                        filetype=extension[1:],
                        book=book,
                        storage_provider='dropbox',
                    )


