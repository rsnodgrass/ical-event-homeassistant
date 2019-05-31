"""
Support for Flo water inflow monitoring and control devices

FUTURE:
- last health test timestamp
- add switchable mode (home/away/sleep)
- convert to async
"""
import logging

from homeassistant.const import ( TEMP_FAHRENHEIT, ATTR_TEMPERATURE )
from . import FloService, FloEntity

_LOGGER = logging.getLogger(__name__)

ATTR_TOTAL_FLOW = 'total_flow'

# pylint: disable=unused-argument
def setup_platform(hass, config, add_sensors_callback, discovery_info=None):
    """Setup the Flo Water Security System integration"""
    if discovery_info is None:
        return

    flo_service = FloService(config)

    # get a list of all Flo inflow control devices
    response = flo_sevice.get_request('/icds/me')
    # Example response:
    #   { "is_paired": true,
    #     "device_id": "a0b405bfe487",
    #     "id": "2faf8cd6-a8eb-4b63-bd1a-33298a26eca8",
    #     "location_id": "e7b2833a-f2cb-a4b1-ace2-36c21075d493" }
    json = response.json()

    # FUTURE: support multiple devices (and locations)
    sensors = []

    flo_icd_id = json['id']
    sensor = FloRateSensor(flo_service, flo_icd_id)
    sensor.update()  # FIXME: this may be unnecessary
    sensors.append( sensor )

    sensor = FloTempSensor(flo_service, flo_icd_id)
    sensor.update()  # FIXME: this may be unnecessary
    sensors.append( sensor )

    sensor = FloPressureSensor(flo_service, flo_icd_id)
    sensor.update()  # FIXME: this may be unnecessary
    sensors.append( sensor )

    # execute callback to add new entities
    add_sensors_callback(sensors)
        
# FIXME:
# implement a separate sensor for each value vs attributes?
#  https://developers.home-assistant.io/docs/en/entity_sensor.html
#   e.g..  
#   device_class = temperature / unit_of_measurement = 'F'
#   device_class = pressure /  unit_of_measurement = 'psi'

# pylint: disable=too-many-instance-attributes
class FloRateSensor(FloEntity):
    """Water flow rate sensor for a Flo device"""

    def __init__(self, flo_service, flo_icd_id):
        self._flo_icd_id = flo_icd_id
        self._name = 'Water Flow'
        self._state = '0'
        self._attrs = {}
        super().__init__(flo_service)

    @property
    def name(self):
        """Return the display name for this sensor"""
        return self._name

    @property
    def unit_of_measurement(self):
        """Gallons per minute (gpm)"""
        return 'gpm'

    @property
    def state(self):
        """Water flow rate"""
        return self._state

    @property
    def icon(self):
        return 'mdi:water-pump'

    @property
    def device_state_attributes(self):
        """Return the device state attributes."""
        return self._attrs

    def update(self):
        """Update sensor state"""
        json = self._flo_service.get_waterflow_measurement(self._flo_icd_id)

        # FIXME: add sanity checks on response

        self._state = json['average_flowrate']
        self._attrs.update({
            ATTR_TOTAL_FLOW  : json['total_flow']
        })

class FloTempSensor(FloEntity):
    """Water temp sensor for a Flo device"""

    def __init__(self, flo_service, flo_icd_id):
        self._flo_icd_id = flo_icd_id
        self._name = 'Water Temperature'
        self._state = 0
        super().__init__(flo_service)

    @property
    def name(self):
        """Return the display name for this sensor"""
        return self._name

    @property
    def unit_of_measurement(self):
        return TEMP_FAHRENHEIT # FIXME: use correct unit based on Flo device's config

    @property
    def state(self):
        """Water temperature"""
        return self._state

    @property
    def icon(self):
        return 'mdi:thermometer'

    def update(self):
        """Update sensor state"""
        # FIXME: cache results so that for each sensor don't update multiple times
        json = self._flo_service.get_waterflow_measurement(self._flo_icd_id)

        # FIXME: add sanity checks on response

        self._state = json['average_temperature']

class FloPressureSensor(FloEntity):
    """Water pressure sensor for a Flo device"""

    def __init__(self, flo_service, flo_icd_id):
        self._flo_icd_id = flo_icd_id
        self._name = 'Water Pressure'
        self._state = 0
        super().__init__(flo_service)

    @property
    def name(self):
        """Return the display name for this sensor"""
        return self._name

    @property
    def unit_of_measurement(self):
        """Pounds per square inch (psi)"""
        return 'psi'

    @property
    def state(self):
        """Water pressure"""
        return self._state

    @property
    def icon(self):
        return 'mdi:gauge'

    def update(self):
        """Update sensor state"""
        # FIXME: cache results so that for each sensor don't update multiple times
        json = self._flo_service.get_waterflow_measurement(self._flo_icd_id)

        # FIXME: add sanity checks on response

        self._state = json['average_pressure']