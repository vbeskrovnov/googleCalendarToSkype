from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from dateutil import parser

import datetime
import json

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

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
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def getService():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    return discovery.build('calendar', 'v3', http=http)


def getEvents(calendarId):
    service = getService()

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    eventsResult = service.events().list(
        calendarId=calendarId, timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()

    return eventsResult.get('items', [])


def getEventDate(event):
    return event['start'].get('dateTime', event['start'].get('date'))


def getEventName(event):
    return event['summary']


def getEventsJson(events):
    result = []
    for event in events:
        data = {
            'name': getEventName(event),
            'date': getEventDate(event),
            'notification': []}
        result.append(data)
    return result


def getEventsFromFile(fileName):
    eventsFile = open(fileName, 'r+')
    oldEventsStr = eventsFile.read()
    eventsFile.close()
    oldEvents = []
    if oldEventsStr != '':
        oldEvents = json.loads(oldEventsStr)
    return oldEvents


def saveEventsToFile(fileName, events):
    eventsFile = open(fileName, 'r+')
    eventsFile.seek(0)
    eventsFile.truncate()
    eventsFile.write(json.dumps(events))
    eventsFile.close()


def updateEvents(events, fileName):
    events = getEventsJson(events)

    oldEvents = getEventsFromFile(fileName)

    for event in events:
        if isEventExist(oldEvents, event):
            event['notification'] = getEvent(oldEvents, event['name'])['notification']

    saveEventsToFile(fileName, events)
    return


def isEventExist(events, event):
    for oldEvent in events:
        if oldEvent['name'] == event['name']:
            return True
    return False


def getEvent(events, name):
    for event in events:
        if event['name'] == name:
            return event
    return None
