import datetime
import os.path
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
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

def refresh_meetings(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    meetings = get_upcoming_meetings()
    
    if not meetings:
        label = ttkb.Label(frame, text="No upcoming Google Meet meetings found.", font=('Helvetica', 12), bootstyle="danger")
        label.pack(pady=20)
    else:
        for meeting in meetings:
            meeting_info = f"{meeting['summary']} - {meeting['start']}\nLink: {meeting['link']}"
            
            # Add a rounded "card" style frame for each meeting
            meeting_frame = ttkb.Frame(frame, padding=10, bootstyle="secondary", borderwidth=1, relief="solid")
            meeting_frame.pack(fill="x", padx=10, pady=10)
            
            # Meeting info with a larger summary and a smaller start time
            title = ttkb.Label(meeting_frame, text=meeting['summary'], font=('Helvetica', 14, 'bold'), bootstyle="primary")
            title.pack(anchor="w")
            
            time_label = ttkb.Label(meeting_frame, text=meeting['start'], font=('Helvetica', 10), bootstyle="secondary")
            time_label.pack(anchor="w", pady=5)

            # Show the Google Meet link as a button for easy access
            link_button = ttkb.Button(meeting_frame, text="Join Meeting", bootstyle="info-outline", command=lambda l=meeting['link']: open_meeting(l))
            link_button.pack(anchor="w", pady=5)

    frame.after(60000, lambda: refresh_meetings(frame))

def open_meeting(link):
    import webbrowser
    webbrowser.open(link)

def show_meetings():
    app = ttkb.Window(themename="darkly")
    app.title("Upcoming Google Meet Meetings")
    app.geometry("400x500")
    
    title_label = ttkb.Label(app, text="Google Meet Meetings", font=('Helvetica', 18, 'bold'), bootstyle="primary")
    title_label.pack(pady=20)

    frame = ttkb.Frame(app, padding=10)
    frame.pack(fill="both", expand=True)

    refresh_meetings(frame)
    
    # Create a scrollable window for overflow meetings
    canvas = tk.Canvas(app)
    scrollbar = ttkb.Scrollbar(app, orient="vertical", command=canvas.yview)
    scrollable_frame = ttkb.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    app.mainloop()

if __name__ == "__main__":
    show_meetings()
