# Django Gmail API backend

Email backend for Django which sends email via the Gmail API


The simple SMTP protocol is disabled by default for Gmail users, since this
is included in the Less Secure Apps (LSA) category.
The advice is to use SMTP+OAuth or to use the Gmail API directly.
This package implements the second option as a Django email backend.


## Installation

Install the package

```
pip install django-gmailapi-backend
```

## Configuration

In your `settings.py`:

1. Add the module into the `INSTALLED_APPS`
    ```py
    INSTALLED_APPS = [
        ...
        'gmailapi_backend',
        ...
    ]
    ```

2. Set the email backend
    ```py
    EMAIL_BACKEND = 'gmailapi_backend.mail.GmailBackend'
    ```

3. Define the configuration parameters from your Gmail developer account (see next section)
    ```py
    GMAIL_API_CLIENT_ID = 'client_id'
    GMAIL_API_CLIENT_SECRET = 'client_secret'
    GMAIL_API_REFRESH_TOKEN = 'refresh_token'
    ```

## Configure the Gmail credentials

For using this package you need to obtain the OAuth credentials for a valid Gmail account.

- More information on the Gmail API: https://developers.google.com/gmail/api/guides/sending
- OAuth credentials for sending emails: https://github.com/google/gmail-oauth2-tools/wiki/OAuth2DotPyRunThrough

This package includes the script linked in the documentation above, which simplifies
the setup of the API credentials. The following outlines the key steps:

1. Create a project in the Google developer console, https://console.cloud.google.com/
2. Enable the Gmail API
3. Create OAuth 2.0 credentials
4. Create a valid `refresh_token` using the helper script included in the package:
    ```sh
    gmail_oauth2 --generate_oauth2_token \
      --client_id="<client_id>" \
      --client_secret="<client_secret>" \
      --scope="https://www.googleapis.com/auth/gmail.send"
    ```

