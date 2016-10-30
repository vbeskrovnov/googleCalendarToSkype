import parser
import skyper
import datetime
from dateutil.parser import parse
import time
import properties

def getRemainingTime(date):
    return parse(date).replace(tzinfo=None) - datetime.datetime.now()

def main():
    while True:
        events = parser.getEvents(properties.google_url)
    
        if not events:
            print('No upcoming events found.')

        sendNotify(events)
        time.sleep(600)


def sendNotify(events):
    parser.updateEvents(events, properties.events_file_name)
    events = parser.getEventsFromFile(properties.events_file_name)
    for event in events:
        notification = event['notification']
        name = event['name']
        date = event['date']
        formatedDate = parse(date).strftime(properties.date_formatting)
        if 'init' not in notification:
            skyper.sendMessage(properties.init_message.format(name, formatedDate))
            notification.append('init')
        if '2day' not in notification and getRemainingTime(date).days == 2:
            skyper.sendMessage(properties.two_day_message.format(name, formatedDate))
            notification.append('2day')
        if '1day' not in notification and getRemainingTime(date).days == 1:
            skyper.sendMessage(properties.one_day_message.format(name, formatedDate))
            notification.append('1day')
        if '2hour' not in notification and getRemainingTime(date).seconds / 60 / 60 == 1:
            skyper.sendMessage(properties.two_hours_message.format(name, formatedDate))
            notification.append('2hour')
        if '1hour' not in notification and getRemainingTime(date).seconds / 60 / 60 == 0:
            skyper.sendMessage(properties.one_hours_message.format(name, formatedDate))
            notification.append('1hour')
    parser.saveEventsToFile(properties.events_file_name, events)


if __name__ == '__main__':
    main()
