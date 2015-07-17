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


def parse_folder(client, path):
    print("working on {}".format(path))
    metadata = client.metadata(path)
    if not metadata.get('is_dir'):
        parse_item(metadata)
    else: 
        for item in metadata.get('contents'):
            if not item.get('is_dir'):
                parse_item(item)
            else:
                parse_folder(client, item.get('path'))


def parse_item(item):
    if item.get('mime_type') in MIMETYPES:
        filename = item.get('path').split('/')[-1]
        name, extension = os.path.splitext(filename)
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