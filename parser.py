
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from dateutil import parser

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def getDateDif(fromDate, toDate):
    return fromDate - toDate;

def getService():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    return discovery.build('calendar', 'v3', http=http)

def getEvents(calendarId):
    service = getService()

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId=calendarId, timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()

    return eventsResult.get('items', []) 

def main():
    service = getService()

    nowTime = datetime.datetime.utcnow() 
    now = nowTime.isoformat() + 'Z' # 'Z' indicates UTC time
    
    events = getEvents('h3qa9705p4v3sd7275l4cbjg20@group.calendar.google.com')
    
    if not events:
        print('No upcoming events found.')
    
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        print(getDateDif(parser.parse(start).replace(tzinfo=None), nowTime))

if __name__ == '__main__':
    main()
