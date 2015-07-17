import dropbox
import json

from django.conf import settings
from django.core.management.base import BaseCommand

from books.utils import parse_folder


class Command(BaseCommand):
    help = "add books from dropbox to the db"

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
        parse_folder(self.client, '/eBooks/sortme/McCaffrey, Anne')
