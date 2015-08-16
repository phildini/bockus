import dropbox
import json

from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage

from allauth.socialaccount.models import SocialToken

from books.utils import (
    parse_folder,
)

from libraries.models import LibraryImport


class Command(BaseCommand):
    help = "get import job and run it"

    def handle(self, *args, **options):
        library_import_jobs = LibraryImport.objects.filter(
            status=LibraryImport.PENDING)[:4]

        for job in library_import_jobs:
            job.status = LibraryImport.PROCESSING
            job.save()
            token = None
            try:
                token = SocialToken.objects.get(
                    account__user=job.librarian.user,
                    app__provider='dropbox_oauth2',
                ).token
            except:
                job.status = LibraryImport.ERROR
                job.save()

            if token:
                client = dropbox.client.DropboxClient(token)
                parse_folder(
                    client=client,
                    path=job.path,
                    library=job.librarian.library,
                    user=job.librarian.user,
                )
                job.status = LibraryImport.DONE
                job.save()
