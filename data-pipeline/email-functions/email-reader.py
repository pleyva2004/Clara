import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Gets an authorized Gmail API service instance."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
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

def get_latest_email_from_sender(sender_email):
    """Retrieves the latest email from a specific sender."""
    service = get_gmail_service()
    
    # Search for emails from the specific sender
    query = f'from:{sender_email}'
    results = service.users().messages().list(userId='me', q=query, maxResults=1).execute()
    messages = results.get('messages', [])
    
    if not messages:
        print(f'No emails found from {sender_email}')
        return None
    
    # Get the latest message
    msg = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
    
    # Extract email content
    if 'payload' in msg and 'parts' in msg['payload']:
        parts = msg['payload']['parts']
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                text = base64.urlsafe_b64decode(data).decode()
                return text
    elif 'payload' in msg and 'body' in msg['payload']:
        data = msg['payload']['body']['data']
        text = base64.urlsafe_b64decode(data).decode()
        return text
    
    return None

if __name__ == '__main__':
    sender_email = 'pl33@njit.edu'
    latest_email = get_latest_email_from_sender(sender_email)
    
    if latest_email:
        print("Latest email content:")
        print(latest_email)
    else:
        print("No email content found")
