import pytz
import requests
from settings import MEETUP_KEY, MEETUP_GROUP_URLNAME
import json

from datetime import datetime

BASE_URL = 'https://api.meetup.com/'
ALL_EVENTS_URL = '2/events'
EVENT_DETAIL_URL = '2/event/{0}/'

def get_num_of_hours(time_in_milliseconds):
    '''
    :param time_in_milliseconds: as it sounds :-)
    :return: num_of_hours (3600000 ms per hour)
    '''
    return time_in_milliseconds / 3600000

def get_human_readable_date(time):
        '''
        :param time: is an epoch time string length 10
        '''
        naive = datetime.utcfromtimestamp(time)
        tz = pytz.timezone("America/Chicago")
        tzoffset = tz.utcoffset(naive)
        localized = tzoffset + naive
        return localized.strftime('%Y-%m-%d %I:%M')

def get_meetup_events():
    '''
    Docs: http://www.meetup.com/meetup_api/docs/2/events/
    Where find your API key: https://secure.meetup.com/meetup_api/key/
    '''
    query_params = '?key=%s&group_urlname=%s' % (MEETUP_KEY, MEETUP_GROUP_URLNAME)
    events_response = requests.get(BASE_URL + '2/events' + query_params)
    events = json.loads(events_response.content).get('results', None) # two keys returned meta & results

    active_events = {}

    for event in events:
        if event.get('status', None) == 'upcoming':
            active_events[event['id']] = {  'name': event.get('name', 'Check MeetUp'),
                                            # 'status': event.get('status', 'Check MeetUp'),
                                            'event_url': event.get('event_url', 'Check MeetUp'),
                                            'start_time': int(event.get('time',0)) / 1000, # event['time'] / 1000 as time is an epoch time string length of length 13
                                            'duration': get_num_of_hours(event.get('duration', 0)),
                                            'attendee_count': event.get('rsvp_limit', 0) }

    return active_events

def get_meetup_address(event_id):
    '''http://www.meetup.com/meetup_api/docs/2/event/#get'''
    query_params = '?key={0}'.format(MEETUP_KEY)

    request_url = BASE_URL + EVENT_DETAIL_URL.format(event_id) + query_params

    event_response = requests.get(request_url)
    event_info = json.loads(event_response.content).get('venue', None)

    try:
        address = event_info['address_1'] + ', ' + event_info['city'] + ', ' + event_info['state']
        name = event_info['name']
    except:
        address = 'Chicago, Illinois'
        name = "Chicago"

    return address, name

def get_user(user_id):
    from app.models import User
    return User.query.get(user_id)