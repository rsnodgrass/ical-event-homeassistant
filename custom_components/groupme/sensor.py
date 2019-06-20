"""
Tracks GroupMe message state
"""
import logging
import datetime as dt
from datetime import datetime, timedelta
from groupy.client import Client

import requests

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)
REQUIREMENTS = ['GroupyAPI', 'requests', 'arrow>=0.10.0']

VERSION = "0.0.1"
PLATFORM = 'groupme'
DEFAULT_SENSOR_NAME = 'groupme'
DEFAULT_STATE = 'Unknown'
SCAN_INTERVAL = timedelta(minutes=1)

# FIXME: switch to async_setup_platform, see
#  https://developers.home-assistant.io/docs/en/asyncio_working_with_async.html
def setup_platform(hass, config, add_entities, discovery_info=None):
    """Initialize the sensor defaults"""

    # sanity check the HASS configuration
    token = config.get('token')
    if (token is None):
        _LOGGER.error("Missing required configuration 'token' containing GroupMe access token")
        return False

    sensor_name = config.get('name', DEFAULT_SENSOR_NAME)

    sensors = []
    sensors.append(GroupMeSensor(hass, config, sensor_name))
    add_entities(sensors)

DEFAULT_ATTRIBUTES = {
    'start': None,
    'end': None
}

# pylint: disable=too-few-public-methods
class GroupMeSensor(Entity):
    def __init__(self, hass, config, sensor_name):
        """
        Initialize the Home Assistant sensor.
        """
        self._hass = hass
        self._config = config
        self._name = sensor_name
        self._events = []

        self._default_state = config.get('default', DEFAULT_STATE)
        self._state = self._default_state
        self._attributes = DEFAULT_ATTRIBUTES

        # trigger an update from the data source
        self._groupme = GroupMe(config)
        self.update()

    @property
    def name(self):
        """Return the sensor's name"""
        return self._name

    @property
    def icon(self):
        """Return the sensor's icon"""
        return 'mdi:message'

    @property
    def state(self):
        """Return the sensor's state"""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the sensor's attributes"""
        return self._attributes

    # FUTURE: implement async def async_update(self)
    def update(self):
        """Update the latest state and attributes for this sensor."""
        self._groupme.update() # blocking call, convert to async in future

        self._state = self._default_state
        self._attributes = DEFAULT_ATTRIBUTES

        _LOGGER.info("Updated sensor '%s' to '%s'", self_.name, self_.state)

# pylint: disable=too-few-public-methods
class GroupMe(object):
    def __init__(self, config):
        self._client = Client.from_token(config.get('token'))
        self._groups = []

        for group in client.groups.list(omit="memberships")
          if group.id == '49117054'
            self._groups.append( group )

    # FUTURE: make the throttle interval configurable, based on refresh_interval in HA
    @Throttle(timedelta(seconds=120)) # return cached data if updated < 2 minutes ago
    def update(self):
        source = 'GroupMe'
        try:

            # only load 'recent' messages
            for message in group.messages.list()
              _LOGGER.info("Found message %s", message)

        except requests.exceptions.RequestException:
            _LOGGER.error("Error fetching data from %s", source)
            self.events = []
