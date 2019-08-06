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

# see https://www.troublefreepool.com/blog/2018/12/12/abcs-of-pool-water-chemistry/
POOL_MATH_SENSOR_SETTINGS = {
    'fc':     { 'name': 'FC',     'units': 'mg/L', 'description': 'Free Chlorine'    },
    'ph':     { 'name': 'pH',     'units': 'pH',   'description': 'Acidity/Basicity' },
    'ta':     { 'name': 'TA',     'units': 'ppm',  'description': 'Total Alkalinity' },
    'ch':     { 'name': 'CH',     'units': 'ppm',  'description': 'Calcium Hardness' },
    'cya':    { 'name': 'CYA',    'units': 'ppm',  'description': 'Cyanuric Acid'    },
    'salt':   { 'name': 'Salt',   'units': 'ppm',  'description': 'Salt'             },
    'borate': { 'name': 'Borate', 'units': 'ppm',  'description': 'Borate'           }
}

TFP_RECOMMENDED_TARGET_LEVELS = {
    'fc':     { 'min': 0,    'max': 0    }, # depends on CYA
    'ph':     { 'min': 7.2,  'max': 7.8, 'target': 7.7 },
    'ta':     { 'min': 0,    'max': 0    },
    'ch':     { 'min': 250,  'max': 350  }, # with salt: 350-450 ppm
    'cya':    { 'min': 30,   'max': 50   }, # with salt: 70-80 ppm
    'salt':   { 'min': 2000, 'max': 3000 },
    'borate': { 'min': 30,   'max': 50   },
}

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Web scrape sensor."""
    client = PoolMathClient(config)

class PoolMathClient():
    def __init__(self, config):
        verify_ssl = True

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

    def get_sensor(self, sensor_type):
        sensor = self._sensors[sensor_type]
        if sensor:
            return sensor

        config = POOL_MATH_SENSOR_SETTINGS[sensor_type]
        if config is None:
            log.info(f"Unknown Pool Math sensor '{sensor_type}' discovered at {self._url}")
            return None

        name = self._name + " " + config['name']
        sensor = PoolMathSensor(self, name, config['units'])
        self._sensors[sensor_type] = sensor

        # register sensor with Home Assistant
        # FIXME: is there a way to specify the update interval (or disable it!?)
        add_entities([sensor], True)
        return sensor

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
            sensor_type = 'unknown'
            state = 'unknown'
            for div in entry.find_all('div'):
                if div['class'] == 'bold':
                    state = div.string
                else:
                    sensor_type = div['class']
            
            log.warn(f"Found sensor type {sensor_type} = {state}")
            sensor = get_sensor(sensor_type)
            if sensor:
                sensor.inject_state(state)

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