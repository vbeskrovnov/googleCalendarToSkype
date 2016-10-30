import parser
import skyper
import datetime
from dateutil.parser import parse


def getRemainingTime(date):
    return parse(date).replace(tzinfo=None) - datetime.datetime.now()

def main():
    events = parser.getEvents('h3qa9705p4v3sd7275l4cbjg20@group.calendar.google.com')
    
    if not events:
        print('No upcoming events found.')
    
    parser.updateEvents(events,'events.json')
    
    events = parser.getEventsFromFile('events.json')
    
    for event in events:
        print(getRemainingTime(event['date']).seconds/60)
        notification = event['notification']
        name = event['name']
        if 'init' not in notification:
            skyper.sendMessage(name)
            notification.append('init')     
        if '2day' not in notification and getRemainingTime(event['date']).days == 2:
            skyper.sendMessage(name + ' 2 day')
            notification.append('2day')
        if '1day' not in notification and getRemainingTime(event['date']).days == 1:
            skyper.sendMessage(name + ' 1 day')
            notification.append('1day')
        if '2hour' not in notification and getRemainingTime(event['date']).seconds/60/60 == 1:
            skyper.sendMessage(name + ' 2 hour')
            notification.append('2hour')
        if '1hour' not in notification and getRemainingTime(event['date']).seconds/60/60 == 0:
            skyper.sendMessage(name + ' 1 hour')
            notification.append('1hour')

    parser.saveEventsToFile('events.json', events)
    

if __name__ == '__main__':
    main()
