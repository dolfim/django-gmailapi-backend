"""
Email backend that uses the GMail API via OAuth2 authentication.
"""
import base64
import logging

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address

import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
        self.service = build('gmail', 'v1', credentials=credentials)

    def send_message(self, message):
        if not message.recipients():
            return False
        encoding = message.encoding or settings.DEFAULT_CHARSET
        # from_email = sanitize_address(message.from_email, encoding)
        # recipients = [sanitize_address(addr, encoding) for addr in message.recipients()]
        # message = message.message()
        raw_message = {'raw': base64.urlsafe_b64encode(message.message().as_string().encode()).decode()}
        try:
            self.service.users().messages().send(userId=self.user_id, body=raw_message).execute()
            return True
        except HttpError as error:
            logger.exception('An error occurred sending the message via GMail API')
        return False

    def send_messages(self, email_messages):
        """Write all messages to the stream in a thread-safe way."""
        if not email_messages:
            return 0
        msg_count = 0
        try:
            for message in email_messages:
                self.send_message(message)
                msg_count += 1
        except Exception:
            if not self.fail_silently:
                raise
        return msg_count