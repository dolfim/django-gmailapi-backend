"""
Email backend that uses the GMail API via OAuth2 authentication.
"""
import base64
import logging

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

import google.oauth2.credentials
import googleapiclient.discovery

logger = logging.getLogger(__name__)


class GmailBackend(BaseEmailBackend):
    def __init__(self, client_id=None, client_secret=None, refresh_token=None,
                 user_id=None, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        self.client_id = client_id or settings.GMAIL_API_CLIENT_ID
        self.client_secret = client_secret or settings.GMAIL_API_CLIENT_SECRET
        self.refresh_token = refresh_token or settings.GMAIL_API_REFRESH_TOKEN
        if hasattr(settings, 'GMAIL_API_USER_ID'):
            self.user_id = user_id or settings.GMAIL_API_USER_ID
        else:
            self.user_id = user_id or 'me'

        credentials = google.oauth2.credentials.Credentials(
            'token',
            refresh_token=self.refresh_token,
            token_uri='https://accounts.google.com/o/oauth2/token',
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        self.service = googleapiclient.discovery.build('gmail', 'v1', credentials=credentials, cache_discovery=False)

    def send_message(self, email_message):
        if not email_message.recipients():
            return False
        message = email_message.message()
        if email_message.bcc:
            email_message._set_list_header_if_not_empty(message, 'Bcc', email_message.bcc)
        raw_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        return self.service.users().messages().send(userId=self.user_id, body=raw_message)

    def send_messages(self, email_messages):
        """Send all messages using BatchHttpRequest"""
        if not email_messages:
            return 0
        msg_count = 0
        last_exception = None

        def send_callback(r_id, response, exception):
            nonlocal msg_count, last_exception
            if exception is not None:
                logger.exception('An error occurred sending the message via GMail API:  %s', exception)
                last_exception = exception
            else:
                msg_count += 1

        batch = self.service.new_batch_http_request(send_callback)
        for message in email_messages:
            batch.add(self.send_message(message))
        batch.execute()
        if not self.fail_silently and last_exception:
            raise last_exception
        return msg_count
