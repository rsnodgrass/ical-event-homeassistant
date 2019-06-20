"""
Support for Flo water inflow monitoring and control devices

FUTURE:
- convert to async
- use track_point_in_utc_time() to trigger and update every 16 minutes
     (one minute after Flo's every 15 minute average rollup)
"""
import logging

from homeassistant.const import ( TEMP_FAHRENHEIT, ATTR_TEMPERATURE )
from . import FloService, FloEntity

_LOGGER = logging.getLogger(__name__)

ATTR_TIME       = 'time'
ATTR_TOTAL_FLOW = 'total_flow'

#SCAN_INTERVAL = timedelta(seconds=0.1)

# pylint: disable=unused-argument
def setup_platform(hass, config, add_sensors_callback, discovery_info=None):
    """Setup the Flo water inflow control sensor"""
    flo_service = FloService(config)

    # get a list of all Flo inflow control devices
    response = flo_service.get_request('/icds/me')
    # Example response:
    #   { "is_paired": true,
    #     "device_id": "a0b405bfe487",
    #     "id": "2faf8cd6-a8eb-4b63-bd1a-33298a26eca8",
    #     "location_id": "e7b2833a-f2cb-a4b1-ace2-36c21075d493" }
    json_response = response.json()
    flo_icd_id = json_response['id']

    # FUTURE: support multiple devices (and locations)
    sensors = []
    sensors.append(FloRateSensor(flo_service, flo_icd_id))
    sensors.append(FloTempSensor(flo_service, flo_icd_id))
    sensors.append(FloPressureSensor(flo_service, flo_icd_id))
#    sensors.append(FloModeSensor(flo_service, flo_icd_id))

    for sensor in sensors:
        sensor.update()

    # execute callback to add new entities
    add_sensors_callback(sensors)

# pylint: disable=too-many-instance-attributes
class FloRateSensor(FloEntity):
    """Water flow rate sensor for a Flo device"""

    def __init__(self, flo_service, flo_icd_id):
        self._flo_icd_id = flo_icd_id
        self._name = 'Flo Water Flow Rate'
        self._state = 0.0
        super().__init__(flo_service)

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

    def update(self):
        """Update sensor state"""
        json_response = self._flo_service.get_waterflow_measurement(self._flo_icd_id)

        # FIXME: add sanity checks on response

        self._state = float(json_response['average_flowrate'])
        self._attrs.update({
            ATTR_TOTAL_FLOW  : round(float(json_response['total_flow']),1),
            ATTR_TIME        : json_response['time']
        })
        _LOGGER.info("Updated %s to %f %s : %s", self._name, self._state, self.unit_of_measurement, json_response)

class FloTempSensor(FloEntity):
    """Water temp sensor for a Flo device"""

    def __init__(self, flo_service, flo_icd_id):
        self._flo_icd_id = flo_icd_id
        self._name = 'Flo Water Temperature'
        self._state = 0.0
        super().__init__(flo_service)

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
        json_response = self._flo_service.get_waterflow_measurement(self._flo_icd_id)

        # FIXME: add sanity checks on response

        # FUTURE: round just to nearest degree?
        self._state = round(float(json_response['average_temperature']), 1)
        self._attrs.update({
            ATTR_TIME        : json_response['time']
        })
        _LOGGER.info("Updated %s to %f %s : %s", self._name, self._state, self.unit_of_measurement, json_response)


class FloPressureSensor(FloEntity):
    """Water pressure sensor for a Flo device"""

    def __init__(self, flo_service, flo_icd_id):
        self._flo_icd_id = flo_icd_id
        self._name = 'Flo Water Pressure'
        self._state = 0.0
        super().__init__(flo_service)

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
        json_response = self._flo_service.get_waterflow_measurement(self._flo_icd_id)

        # FIXME: add sanity checks on response

        self._state = round(float(json_response['average_pressure']), 1)
        self._attrs.update({
            ATTR_TIME        : json_response['time']
        })
        _LOGGER.info("Updated %s to %f %s : %s", self._name, self._state, self.unit_of_measurement, json_response)

class FloModeSensor(FloEntity):
    """Sensor returning current monitoring mode for the Flo device"""

    def __init__(self, flo_service, flo_icd_id):
        self._flo_icd_id = flo_icd_id
        self._name = 'Flo Water Monitoring'
        self._state = 'Away'
        super().__init__(flo_service)

    @property
    def unit_of_measurement(self):
        """Mode: Home, Away, Sleep"""
        return 'mode'

    @property
    def state(self):
        """Flo water monitoring mode"""
        return self._state

    @property
    def icon(self):
        return 'mdi:shield-search'

    def update(self):
        """Update sensor state"""
    
        # FIXME: cache results so that for each sensor don't update multiple times
        json_response = self._flo_service.get_request('/icdalarmnotificationdeliveryrules/scan')
        _LOGGER.info("Flo alarm notification: " + json_response)
