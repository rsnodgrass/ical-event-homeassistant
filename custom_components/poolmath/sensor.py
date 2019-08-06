import logging

import voluptuous as vol
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.components.rest.sensor import RestData
from homeassistant.const import (
    CONF_NAME,
    CONF_URL
)
from homeassistant.helpers.entity import Entity
from homeassistant.exceptions import PlatformNotReady
import homeassistant.helpers.config_validation as cv

from bs4 import BeautifulSoup

log = logging.getLogger(__name__)

DEFAULT_NAME = 'Pool Math'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_RESOURCE): cv.string
    }
)

# for each type of data log returned, create a sensor and add it
SENSOR_UNITS = {  # units or names?
    'fc': 'FC',
    'ph': 'pH',
    'ta': 'TA',
    'ch': 'CH',
    'cya': 'CYA',
    'salt': 'Salt'
}

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Web scrape sensor."""
    url = config.get(CONF_RESOURCE)

    client = PoolMathClient(config)

    # FIXME: create a sensor for each value?
#    add_entities(
#        [PoolMathSensor(rest, name, select, attr, index, value_template, unit)], True
#    )

class PoolMathClient():
    def __init__(self, config):
        verify_ssl = False

        self._url = config.get(CONF_URL)
        self._rest = RestData('GET', self._url, '', '', '', verify_ssl)

        self._rest.update()
        if self._rest.data is None:
            raise PlatformNotReady

        self._raw_data = BeautifulSoup(self._rest.data, 'html.parser')

        self._name = config.get(CONF_NAME)
        if self._name == None:
            self._name = DEFAULT_NAME

            pool_name = raw_data.select('body.h1').string
            if pool_name != None:
                self._name += " " + pool_name
                log.info(f"Loaded Pool Math data for '{pool_name}'")

        log.info(f"Created Pool Math sensor: {self._name}")
        self._sensors = {}
        self._update_sensors()

    # FIXME: don't update more frequently than a configured interval
    
    def update():
        self._rest.update()
        if self._rest.data is None:
            log.warning(f"Failed to update Pool Math data for '{self._name}' from {self._url}")
            return

        self._raw_data = BeautifulSoup(self._rest.data, 'html.parser')
        self._update_sensors()

    def _update_sensors():
        most_recent_test_log = raw_data.find('div', class_='testLogCard')
        log.info(f"Most recent test log entry: {most_recent_test_log}")

        if most_recent_test_log == None:
         log.info(f"Couldn't find any test logs at {url}")
            raise PlatformNotReady

        # capture the time the most recent Pool Math data was collected
        self._timestamp = most_recent_test_log.find('time', class_='timestamp timereal')
        log.info(f"Timestamp for most recent test log: {self._timestamp}")

        # iterate through all the data chiclets and dynamically create sensors
        data_entries = most_recent_test_log.find(class_='chiclet')
        for entry in data_entries:
            #bold is data... other is which sensor result
            log.info(f"Entry = {entry}")
            sensor_type = 'fc'

    def get_name(self):
        return self._name 

class UpdatableSensor(Entity):
    """Representation of a sensor whose state is kept up-to-date by an external data source."""

    def __init__(self, data_source, name, unit_of_measurement):
        """Initialize the sensor."""
        self._data_source = data_source

        self._name = name
        self._unit_of_measurement = unit_of_measurement
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    def inject_state(self, state)
        self._state = state

    def update(self):
        """Get the latest data from the source and updates the state."""

        # asynchronously trigger an update of this sensor (and all related sensors)
        self._data_source.update()