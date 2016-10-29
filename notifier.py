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
    
    events = parser.getOldEventsJson('events.json')
    
    for event in events:
        print(getRemainingTime(event['date']))
        notification = event['notification']
        if 'init' not in notification:
            skyper.sendMessage(event['name'])
            notification.append('init')     
        if '2day' not in notification and getRemainingTime(event['date']).days == 2:
            skyper.sendMessage(event['name'] + ' 2 day')
            notification.append('2day')
        if '1day' not in notification and getRemainingTime(event['date']).days == 1:
            skyper.sendMessage(event['name'] + ' 1 day')
            notification.append('1day')
    print(events)
    

if __name__ == '__main__':
    main()
