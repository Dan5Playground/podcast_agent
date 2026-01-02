import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

import re

def extract_latest_entry(full_text):
    # Split the text by the marker
    marker = "######"
    
    if marker in full_text:
        # split() returns a list; [0] is everything before the marker
        latest_entry = full_text.split(marker)[0].strip()
    else:
        # Fallback: if you forget the marker, take the whole doc
        latest_entry = full_text.strip()
        
    return latest_entry

def get_google_doc_text(doc_id):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('docs', 'v1', credentials=creds)
    document = service.documents().get(documentId=doc_id).execute()
    
    # Extracting only the text content
    content = document.get('body').get('content')
    full_text = ""
    for value in content:
        if 'paragraph' in value:
            for elements in value.get('paragraph').get('elements'):
                full_text += elements.get('textRun', {}).get('content', '')
    return full_text


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv('api_key.env')
    doc_id = os.getenv("GOOGLE_DOC_ID")
    print(f"Fetching Doc: {doc_id}")
    text = get_google_doc_text(doc_id)
    print("--- CONTENT START ---")
    print(text)
    print("--- CONTENT END ---")
    # test the extraction function
    latest_entry = extract_latest_entry(text)
    print("--- LATEST ENTRY START ---")
    print(latest_entry)
