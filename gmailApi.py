from __future__ import print_function
import pickle
import os.path
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
from googleapiclient.discovery import build  # pip install google-api-python-client
from google_auth_oauthlib.flow import InstalledAppFlow  # pip install google-auth-oauthlib
from google.auth.transport.requests import Request

# 1st run : delete token.pickle, then run script 1-2 times

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']


def api_setup():
    # --------------------------------------------------------------
    # --------------------- Gmail API setup ------------------------
    # --------------------------------------------------------------
    creds = None
    # The file token.pickle stores the user's access and refresh tokens (created 1st execution)
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)


def compose_draft(sender, to, subject, message, attachment_urls):
    # setup
    service = api_setup()

    # draft
    message = create_message(sender, to, subject, message, attachment_urls)
    create_draft(service, message)


def create_message(sender, to, subject, message_text, attachment_urls):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """
    mime_message = MIMEMultipart()
    joined_message = "".join(map(str, message_text))
    message = MIMEText(joined_message)
    mime_message['to'] = to
    mime_message['from'] = sender
    mime_message['subject'] = subject
    mime_message.attach(message)

    # attachments
    for url in attachment_urls:
        content_type, encoding = mimetypes.guess_type(url)
        main_type, sub_type = content_type.split('/', 1)
        file_name = os.path.basename(url)

        f = open(url, 'rb')

        my_file = MIMEBase(main_type, sub_type)
        my_file.set_payload(f.read())
        my_file.add_header('Content-Disposition', 'attachment', filename=file_name)
        encoders.encode_base64(my_file)

        f.close()

        mime_message.attach(my_file)

    return {'raw': base64.urlsafe_b64encode(mime_message.as_bytes()).decode()}


def create_draft(service, message_body):
    try:
        message = {'message': message_body}
        draft = (service.users().drafts().create(userId='me', body=message).execute())
        print('Draft id: %s\nDraft message: %s' % (draft['id'], draft['message']))
        return draft
    except Exception as error:
        print('An error occurred: %s' % error)
        return None


def copy_spreadsheet(service):
    print("copy spreadsheet unimplemented ", service)
