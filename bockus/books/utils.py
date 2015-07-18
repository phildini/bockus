import dropbox
import json
import os

from books.models import Book, BookFileVersion
from troves.models import Trove, TroveLibrarian

MIMETYPES = (
    "application/pdf",
    "application/x-mobipocket-ebook",
    "application/epub+zip",
)


def parse_folder(client, path, user=None):
    print("working on {}".format(path))
    metadata = client.metadata(path)
    if not metadata.get('is_dir'):
        parse_item(metadata)
    else: 
        for item in metadata.get('contents'):
            if not item.get('is_dir'):
                parse_item(item, user)
            else:
                parse_folder(client, item.get('path'))


def parse_item(item, user=None):
    if item.get('mime_type') in MIMETYPES:
        filename = item.get('path').split('/')[-1]
        name, extension = os.path.splitext(filename)
        try:
            # Do we already know about this file?
            bookfile = BookFileVersion.objects.get(
                path=item.get('path'),
                filetype=extension[1:],
            )
        except BookFileVersion.DoesNotExist:
            try:
                # If not, do we know about another file with the same
                # filename?
                bookfile = BookFileVersion.objects.get(
                    path=item.get('path'),
                )
                # If so, create a new file with the new file type
                new_bookfile = BookFileVersion.objects.create(
                    path=item.get('path'),
                    filetype=extension[1:],
                    book=bookfile.book,
                    storage_provider='dropbox',
                    meta=item,
                )
            except BookFileVersion.DoesNotExist:
                # Apparently you know nothing, Jon Snow
                # Create a new book and book file.
                book = Book.objects.create(
                    title=name,
                )
                bookfile = BookFileVersion.objects.create(
                    path=item.get('path'),
                    filetype=extension[1:],
                    book=book,
                    storage_provider='dropbox',
                    meta=item,
                )