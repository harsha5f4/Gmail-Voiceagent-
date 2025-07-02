import pyttsx3
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    engine = pyttsx3.init()

    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(
        userId='me',
        labelIds=['INBOX'],
        maxResults=5
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
        engine.say("no messges found")
        engine.runAndWait()
    else:
        print('Messages:')
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            snippet=msg_data['snippet']
            print('Snippet:', snippet)
            engine.say("Your email says: " + snippet)
            engine.runAndWait()

if __name__ == '__main__':
    main()