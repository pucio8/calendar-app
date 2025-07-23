import asyncio
from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Importing the settings
from .config import settings

def get_google_auth_flow(redirect_uri: str) -> Flow:
    """
    Creates and returns a Flow object for authentication, using a dynamic redirect_uri.
    """
    return Flow.from_client_secrets_file(
        settings.GOOGLE_CREDENTIALS_PATH,
        scopes=settings.GOOGLE_SCOPES,
        redirect_uri=redirect_uri
    )

class GoogleCalendarService:
    """Class to handle the Google Calendar API"""
    
    def get_credentials_from_session(self, session_creds: dict) -> Credentials:
        """Creates a Credentials object from session data"""
        return Credentials(**session_creds)

    # Generic function to add events
    async def add_calendar_event(self, creds: Credentials, date_str: str, summary: str, color_id: str):
        """
        Adds a personalized event to the calendar.
        """
        try:
            service = build("calendar", "v3", credentials=creds)
            start_time = datetime.fromisoformat(f"{date_str}T07:30:00")
            end_time = start_time + timedelta(hours=1)

            event = {
                "summary": summary,
                "start": {"dateTime": start_time.isoformat(), "timeZone": "Europe/Warsaw"},
                "end": {"dateTime": end_time.isoformat(), "timeZone": "Europe/Warsaw"},
                "colorId": color_id
            }
            
            await asyncio.to_thread(
                service.events().insert(calendarId="primary", body=event).execute
            )
            print(f"🗓️ Dodano wydarzenie '{summary}' dla daty {date_str}")
        
        except HttpError as error:
            print(f"Błąd API Google dla daty {date_str}: {error}")
            raise
