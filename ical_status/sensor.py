"""
Returns the current active iCal calendar event (if any) as the sensor value.
"""
import logging
import datetime as dt
from datetime import datetime, timedelta

import requests

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)
REQUIREMENTS = ['icalevents', 'requests', 'arrow>=0.10.0']

VERSION = "0.0.2"
ICON = 'mdi:calendar'
PLATFORM = 'ical_status'
SCAN_INTERVAL = timedelta(minutes=1)
DEFAULT_NAME = 'Unknown Calendar'
DEFAULT_STATE = 'Unknown'

# FIXME: switch to async_setup_platform, see
#  https://developers.home-assistant.io/docs/en/asyncio_working_with_async.html
def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup the sensor"""

    # sanity check the HASS configuration
    url = config.get('url')
    file = config.get('file')
    if (url is None) and (file is None):
        _LOGGER.error("Missing required configuration 'url' or 'file'")
        return False

    sensor_name = config.get('name', DEFAULT_NAME)

    sensors = []
    sensors.append(ICalEventSensor(hass, config, sensor_name))
    add_entities(sensors)

DEFAULT_ATTRIBUTES = {
    'start': None,
    'end': None,
    'remaining': None
}

# pylint: disable=too-few-public-methods
class ICalEventSensor(Entity):
    """
    Implementation of an iCal event sensor
    """
    def __init__(self, hass, config, sensor_name):
        """
        Initialize the iCal event HASS sensor.
        """
        self._hass = hass
        self._config = config
        self._name = sensor_name
        self._events = []

        self._default_state = config.get('default', DEFAULT_STATE)
        self._state = self._default_state
        self._attributes = DEFAULT_ATTRIBUTES

        # trigger an update from the iCal source
        self._ical_data = ICalData(config)
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
        """Return the state of the sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return sensor attributes."""
        return self._attributes

    # FUTURE: implement async def async_update(self)
    def update(self):
        """Update the latest state and attributes for this sensor."""

        self._ical_data.update() # blocking call

        events = self._ical_data.events
        if events and events[0]:
            event = events[0]
            self._state = event.summary
            self._attributes['start'] = event.start.datetime
            self._attributes['end'] = event.end.datetim
            self._attributes['remaining'] = event.time_left.total_seconds()

            # if > one event, include the number of overlapping in the attributes
            if len(events) > 1:
                self._attributes['overlapping'] = len(events)

        else:
            self._state = self._default_state
            self._attributes = DEFAULT_ATTRIBUTES

# pylint: disable=too-few-public-methods
class ICalData(object):
    """
    Maintains the currently active events from the provided iCal source.
    """
    def __init__(self, config):
        self.events  = []
        self._url    = config.get('url')
        self._file   = config.get('file')

        # optional flag to fix non-standard Apple iCal format
        self._fix_apple_format = config.get('fix_apple_format', False)

    # FUTURE: make the throttle interval configurable, based on refresh_interval in HA
    @Throttle(timedelta(seconds=120)) # return cached data if updated < 2 minutes ago
    def update(self):
        import icalevents

        self.events = []
        try: 
            # NOTE: default_span= is not currently exposed by events() interface,
            # or we could shorten this to just providing the timedelta(minutes=1)
            start_time = datetime.now(UTC)
            end_time = start_time + timedelta(minutes=1)

            # FUTURE:
            #  - use events_async() to do the update asynchronously to not block the
            #    Home Assistant event loop
            #  - use X-HA-SENSOR-NAME as the sensor's name, if supplied
            #  - use X-HA-DEFAULT-VALUE as the sensor's default value, if supplied
            #  - use X-HA-ATTRIBUTES to define additional attributes for the calendar
            #    event, such as "color=green", that apply to a specific event

            if self._file:
                es = events(file=self._file,
                            start=start_time, end=end_time,
                            fix_apple=self._fix_apple_format)
                if es is None:
                    _LOGGER.error('Unable to fetch iCal data from %s', self._file)
                    return False

            if self._url:
                es = events(url=self._url,
                            start=start_time, end=end_time,
                            fix_apple=self._fix_apple_format)
                if es is None:
                    _LOGGER.error('Unable to fetch iCal data from %s', self._url)
                    return False

            self.events = es

        except requests.exceptions.RequestException:
            _LOGGER.error("Error fetching data from url=%s / file=%s", self._url, self._file)
            self.events = []
