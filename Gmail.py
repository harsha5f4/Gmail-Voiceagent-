import os
import pickle
import pyttsx3
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64


SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

def get_gmail_service():
    
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def read_emails(query):

    service = get_gmail_service()

    if query.strip().lower() in ["", "emails", "my emails"]:
        final_query = ""
    else:
        final_query = query

    results = service.users().messages().list(
        userId='me',
        q=final_query,
        #maxResults=10
    ).execute()

    messages = results.get('messages', [])
    snippets = []

    engine = pyttsx3.init()

    if not messages:
        engine.say("No messages found.")
        engine.runAndWait()
    else:
        if final_query == "":
            engine.say("Sure! I will read your emails now.")
        else:
            engine.say(f"Sure! I will read the emails that match: {final_query}.")
        engine.runAndWait()

        for msg in messages:
            msg_data = service.users().messages().get(
                userId='me', id=msg['id']).execute()
            snippet = msg_data['snippet']
            print('Snippet:', snippet)
            engine.say("Your email says: " + snippet)
            engine.runAndWait()

def search_emails(query):
    
    service = get_gmail_service()

    if query.strip().lower() in ["", "emails", "my emails"]:
        final_query = ""
    else:
        final_query = query

    results = service.users().messages().list(
        userId='me',
        q=final_query
        # maxResults=5
    ).execute()

    messages = results.get('messages', [])
    snippets = []

    if not messages:
        print("No messages found.")
    else:
        print(f"Top 5 emails matching: '{final_query}':\n")
        for i, msg in enumerate(messages, start=1):
            msg_data = service.users().messages().get(
                userId='me', id=msg['id']).execute()
            snippet = msg_data['snippet']
            print(f"Email {i}: {snippet}\n")
            snippets.append(snippet)

def write_email(to, subject, body):
    
    service = get_gmail_service()

    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        sent_message = (service.users().messages().send(userId="me", body={'raw': raw_message}).execute())
        engine = pyttsx3.init()
        engine.say(f"Email sent to {to} with subject '{subject}'")
        engine.runAndWait()
        return sent_message
    except Exception as e:
        print(f"An error occurred: {e}")
        engine = pyttsx3.init()
        engine.say("Sorry, I could not send the email.")
        engine.runAndWait()