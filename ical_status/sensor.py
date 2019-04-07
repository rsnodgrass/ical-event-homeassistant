"""
Returns the current active iCal calendar event (if any) as the sensor value.
"""
import logging
import datetime as dt
from datetime import timedelta

import requests

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)
REQUIREMENTS = ['icalendar', 'requests', 'arrow>=0.10.0']

VERSION = "0.0.1"
ICON = 'mdi:calendar'
PLATFORM = 'ical_status'
SCAN_INTERVAL = timedelta(minutes=1)
DEFAULT_NAME = 'Unknown Calendar'

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup the sensor"""
    url  = config.get('url')

    if url is None:
        _LOGGER.error('Missing required variable: "url"')
        return False

    ical_data = ICalData(url)
    ical_data.update()

    if ical_data.events is None:
        _LOGGER.error('Unable to fetch iCal url')
        return False

    default_name = DEFAULT_NAME
    if ical_data.name:
        default_name = ical_data.name
    name = config.get('name', default_name)

    sensors = []
    sensors.append(ICalEventSensor(hass, ical_data, name))
    add_entities(sensors)

def filter_only_active_events(calendar, current_timestamp):
    """
    Given a calendar and timestamp, returns a list of events which the timestamp is within
    (sorted based on the shortest duration remaining).
    """
    import arrow

    events = []
    for item in calendar.walk('VEVENT'):

        if isinstance(item['DTSTART'].dt, dt.date):
            start = arrow.get(item['DTSTART'].dt)
            start = start.replace(tzinfo='local')
        else:
            start = item['DTSTART'].dt

        if isinstance(item['DTEND'].dt, dt.date):
            end = arrow.get(item['DTEND'].dt)
            end = start.replace(tzinfo='local')
        else:
            end = item['DTEND'].dt

        # skip if start date is in the future
        if start.date() > current_timestamp.date():
            continue

        # skip if end date is in the past
        if end.date() < current_timestamp.date():
            continue

        remaining = end - current_timestamp

        event_dict = {
            'name'      : event['SUMMARY'],
            'start'     : start,
            'end'       : end,
            'remaining' : remaining
        }

        events.append(event_dict)

    # sort based on the duration of the event remaining
    sorted_events = sorted(events, key=lambda k: k['remaining'])
    _LOGGER.debug(sorted_events)
    return sorted_events

# pylint: disable=too-few-public-methods
class ICalEventSensor(Entity):
    """
    Implementation of an iCal event sensor
    """
    def __init__(self, hass, ical_data, sensor_name):
        """
        Initialize the sensor.
        """
        self._hass = hass
        self._name = sensor_name
        self._ical_data = ical_data
        self._event_attributes = {}

        self.update()

    @property
    def name(self):
        """Return the sensor's name."""
        return self._name

    @property
    def icon(self):
        """Return the icon."""
        return ICON

    @property
    def state(self):
        """Return the title of the event (if any) as the state."""
        return self._state

    @property
    def device_state_attributes(self):
        """Details about the event."""
        return self._event_attributes

    def update(self):
        """Get the latest update and set the state and attributes."""

        self._state = 'None'
        self._event_attributes = {
            'start': None,
            'end': None
        }

        self._ical_data.update() # refresh the iCal data (note: may be cached)

        event_list = self._ical_data.events
        if event_list:
            val = event_list[0]
            self._state = val.get('name', 'None')
            self._event_attributes['start'] = val['start'].datetime
            self._event_attributes['end'] = val['end'].datetime

# pylint: disable=too-few-public-methods
class ICalData(object):
    """
    iCal data retrieved with 'events' field containing the list of active events
    """
    def __init__(self, resource):
        self._request = requests.Request('GET', resource).prepare()
        self.name = None
        self.events = None

    @Throttle(timedelta(seconds=120)) # return cached data if updated < 2 minutes ago
    def update(self):
        import arrow
        import icalendar

        self.events = []

        try:
            with requests.Session() as sess:
                response = sess.send(self._request, timeout=10)

            cal = icalendar.Calendar.from_ical(response.text)
            self.events = filter_only_active_events(cal, arrow.utcnow())

            # set the name of the calendar (if any)
            name = cal.get('NAME')
            if name:
                self.name = name

        except requests.exceptions.RequestException:
            _LOGGER.error("Error fetching data: %s", self._request)
            self.events = None
