from __future__ import print_function
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

OOO_CALENDAR_ID = 'alan.eu_9fde1qq8ud6d4kkq3etc2vmias@group.calendar.google.com'
AUTH_TOKEN = 'ya29.GlvmBku3N0JXUFCFNSWS48_LN0HHAb5eychF7fRoqfLrDgR7XeCL65AJ13WIJv1x5dIfNBHeBGJMSPWXv8rxL7ata0uEu9PwwdoOoUJOLxrC4MXCNhZUqGQTWMZy'


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = Credentials(token=AUTH_TOKEN)
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    today = datetime.now().date()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)

    print('Getting the weekly events')
    events_result = service.events().list(calendarId=OOO_CALENDAR_ID,
                                          timeMin=start.isoformat() + 'T00:00:00.000Z',
                                          timeMax=end.isoformat() + 'T23:59:59.999Z',
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()
