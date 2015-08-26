import dropbox
import json
import logging
import os
import shutil
import subprocess

from books.models import Book, BookFileVersion
from libraries.models import Library, Librarian

MIMETYPES = (
    "application/pdf",
    "application/x-mobipocket-ebook",
    "application/epub+zip",
)

logger = logging.getLogger('scripts')


class DropboxParser(object):

    def __init__(self, client, library, user):
        self.client = client
        self.library = library
        self.user = user
        self.can_parse = bool(shutil.which('ebook-meta'))
        self.items_parsed = 0
        

    def parse(self, path):
        self.parse_folder(path)
        logger.debug("{} parsed".format(self.items_parsed))

    def parse_folder(self, path):
        metadata = self.client.metadata(path)
        if not metadata.get('is_dir'):
            self.parse_item(item=metadata)
        else: 
            for item in metadata.get('contents'):
                if not item.get('is_dir'):
                    self.parse_item(item=item)
                else:
                    self.parse_folder(path=item.get('path'))

    def parse_item(self, item):
        # Are we supporting this type of book?
        if item.get('mime_type') in MIMETYPES:
            filename = item.get('path').split('/')[-1]
            name, extension = os.path.splitext(filename)
            try:
                # Do we already know about this file?
                bookfile = BookFileVersion.objects.get(
                    path=item.get('path'),
                    filetype=extension[1:],
                )
                book = bookfile.book
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
                    book = bookfile.book
                except BookFileVersion.DoesNotExist:
                    # Apparently you know nothing, Jon Snow
                    # See if we know about a book with the same title.
                    # If not, create a new book and book file.
                    book = Book.objects.create(
                        title=name,
                        library=self.library,
                        added_by=self.user,
                    )

                    bookfile = BookFileVersion.objects.create(
                        path=item.get('path'),
                        filetype=extension[1:],
                        book=book,
                        storage_provider='dropbox',
                        meta=item,
                    )
            if self.can_parse:
                self.parse_ebook_and_update_db(
                    path=item.get('path'),
                    book=book,
                    filename=filename
                )
        self.items_parsed = self.items_parsed + 1

    def parse_ebook_and_update_db(self, path, book, filename):
        file_meta = None
        ebook_meta = None
        name, extension = os.path.splitext(filename)
        if path:
            with self.client.get_file(path) as f:
                with open('/tmp/{}'.format(filename), 'wb') as w:
                    w.write(f.read())
            file_meta = subprocess.check_output(
                ['ebook-meta','/tmp/{}'.format(filename)],
                universal_newlines=True,
            )
            os.remove('/tmp/{}'.format(filename))
        # Get the details from parsing the ebook meta
        if file_meta:
            ebook_meta = {
                info.split(':')[0].strip():info.split(':')[1].strip() for info in file_meta.splitlines()
            }
        if ebook_meta:
            print(ebook_meta)
            if not book.author:
                book.author = ebook_meta.get('Author(s)')
            if not book.title or book.title == name:
                book.title = ebook_meta.get('Title')
            if book.meta:
                meta = json.loads(book.meta)
            else:
                meta = {}
            meta['published'] = ebook_meta.get('Published')
            meta['publisher'] = ebook_meta.get('Publisher')
            book.meta = json.dumps(meta)
            book.save()
