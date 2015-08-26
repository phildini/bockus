import dropbox
import json
import logging

from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage

from allauth.socialaccount.models import SocialToken

from books.utils import DropboxParser

from libraries.models import LibraryImport

logger = logging.getLogger('scripts')


class Command(BaseCommand):
    help = "get import job and run it"

    def handle(self, *args, **options):
        logger.debug('Starting book import cronjob')
        library_import_jobs = LibraryImport.objects.filter(
            status=LibraryImport.PENDING)[:4]
        for job in library_import_jobs:
            logger.debug('Starting import job %s' % job.id)
            job.status = LibraryImport.PROCESSING
            job.save()
            token = None
            try:
                token = SocialToken.objects.get(
                    account__user=job.librarian.user,
                    app__provider='dropbox_oauth2',
                ).token
            except:
                logger.exception(
                    'Error getting dropbox token for import job %s' % job.id
                )
                job.status = LibraryImport.ERROR
                job.save()

            if token:
                client = dropbox.client.DropboxClient(token)
                parser = DropboxParser(
                    client=client,
                    library=job.librarian.library,
                    user=job.librarian.user,
                )
                try:
                    parser.parse(path=job.path)
                    job.status = LibraryImport.DONE
                    job.save()

                    message = EmailMessage(
                        subject='[Booksonas] Import complete!',
                        body="We've finished importing {}, go login to booksonas.com to see your books!".format(job.path),
                        from_email="import@booksonas.com",
                        to=[job.librarian.user.email],
                    )
                    message.send()
                except:
                    logger.exception("Error parsing path")
            logger.debug('Finished import job %s' % job.id)
        logger.debug('Finished book import cronjob')

