import logging
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.utils import timezone


from invites.models import Invitation

logger = logging.getLogger('scripts')

class Command(BaseCommand):
    help = "send invites"

    def handle(self, *args, **options):
        invites_to_send = Invitation.objects.filter(
            status=Invitation.PENDING
        )[:4]

        for invite in invites_to_send:
            logger.debug('Sending invite %s' % (invite.id))
            invite.status = Invitation.PROCESSING
            invite.save()
            try:
                message = EmailMessage(
                    subject="[Booksonas] Invitation to share %s's library" % (invite.sender),
                    body=(
                        "%s has invited you to share their library on Booksonas.\n"
                        "Go to https://%s/invites/accept/%s/ to join!"
                    ) % (
                        invite.sender,
                        Site.objects.get_current().domain,
                        invite.key,
                    ),
                    from_email="invites@booksonas.com",
                    to=[invite.email,],
                )
                message.send()
            except:
                logger.exception('Problem sending invite %s' % (invite.id))
                invite.status = Invitation.ERROR
                invite.save()
                try:
                    if not settings.DEBUG:
                        payload = {
                            'text': 'Error in booksonas invite: {}'.format(job.id)
                        }
                        r = requests.post(
                            settings.SLACK_WEBHOOK_URL,
                            data=json.dumps(payload),
                        )
                except:
                    logger.exception("Error sending error to slack")
            invite.status = Invitation.SENT
            invite.sent = timezone.now()
            invite.save()


