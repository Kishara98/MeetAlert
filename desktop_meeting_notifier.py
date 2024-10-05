import datetime
import os.path
import tkinter as tk
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_google_calendar():
    """Shows basic usage of the Google Calendar API.
    Returns an authenticated service for interacting with Google Calendar."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_upcoming_meetings():
    service = authenticate_google_calendar()
    # Get the current time and one hour ahead
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    one_hour_ahead = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat() + 'Z'
    
    # Call the Calendar API
    events_result = service.events().list(
        calendarId='primary', timeMin=now, timeMax=one_hour_ahead,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    meetings = []
    for event in events:
        if 'hangoutLink' in event:
            meeting_info = {
                'summary': event['summary'],
                'start': event['start'].get('dateTime', event['start'].get('date')),
                'link': event['hangoutLink']
            }
            meetings.append(meeting_info)
    return meetings

def show_meetings():
    root = tk.Tk()
    root.title("Upcoming Google Meet Meetings")
    root.geometry("400x200")
    
    meetings = get_upcoming_meetings()
    if not meetings:
        label = tk.Label(root, text="No upcoming Google Meet meetings found.")
        label.pack(pady=20)
    else:
        for meeting in meetings:
            meeting_info = f"{meeting['summary']} - {meeting['start']}\nLink: {meeting['link']}"
            label = tk.Label(root, text=meeting_info, wraplength=300, justify="left")
            label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    show_meetings()
