"""
Support for Flo Water Security System

SENSORS:
total_flow (cumulative for day)
last health test timestamp

SWITCHES:
mode (home/away/sleep)
water status (on/off)

FUTURE:
- convert to async

NOTE: I believe "icd" is an "inflow control device"
"""
import logging

from homeassistant.const import (
    CONF_USERNAME, CONF_PASSWORD, CONF_NAME, TEMP_FAHRENHEIT, STATE_ON, ATTR_TEMPERATURE
)
from . import FloEntity

_LOGGER = logging.getLogger(__name__)

ATTR_PRESSURE   = 'pressure'
ATTR_TOTAL_FLOW = 'total_flow'

# pylint: disable=unused-argument
def setup_platform(hass, config, add_sensors_callback, discovery_info=None):
    """Setup the Flo Water Security System integration."""
    if discovery_info is None:
        return

    name     = config.get(CONF_NAME, 'Flo Water Monitor')
    username = config[CONF_USERNAME]
    password = config[CONF_PASSWORD]

    sensors = []
    flo_service = FloService(username, password)

    # execute callback to add new entities
    sensors = flo_service.hass_sensors()

    add_sensors_callback(sensors)

# FIXME: move FloService to __init__.py so it can be shared with switch
class FloService():
    def __init__(self, username, password):
        self._auth_token = None
        self._username = username
        self._password = password

        self._hass_sensors = []
        self._initialize_sensors()
        
    def _flo_authentication_token(self):
        if not self._auth_token:
            # authenticate to the Flo API
            #   POST https://api.meetflo.com/api/v1/users/auth
            #   Payload: {username: "your@email.com", password: "1234"}
            _LOGGER.debug("Authenticating to Flo with account %s (refresh interval %d seconds)",
                          self._username, self._refresh_interval)

            auth_url = 'https://api.meetflo.com/api/v1/users/auth'
            payload = {
                'username': self._username,
                'password': self._password
            }
            response = requests.Request('POST', auth_url, data=json.dumps(payload)).prepare()
            # Response: { "token":"caJhb.....",
            #             "tokenPayload": { "user": { "user_id":"9aab2ced-c495-4884-ac52-b63f3008b6c7","email":"your@email.com"},
            #                               "timestamp": 1559246133 },
            #             "tokenExpiration": 86400,
            #             "timeNow": 1559226161 }

            _LOGGER.debug("Flo authentication of %s received %s", self._username, response.json())
            self._auth_token = response.json()['token']

        return self._auth_token

    def _api_get_request(self, url_path):
        headers = { 'authorization': self._flo_authentication_token() }
        url = 'https://api.meetflo.com/api/v1' + url_path
        response = requests.Request('GET', url, headers=headers).prepare()
        _LOGGER.info("Flo GET %s : %s", url, response.content)
        return response

    def _initialize_sensors(self):
        response = self._api_get_request('/icds/me')
        # Response: { "is_paired":true,
        #             "device_id":"a0b405bfe487",
        #             "id":"2faf8cd6-a8eb-4b63-bd1a-33298a26eca8",
        #             "location_id":"e7b2833a-f2cb-a4b1-ace2-36c21075d493" }
        json = response.json()
 
        # FIXME: *actually* support multiple devices (and locations)
        flo_icd_id = json['id']

        # FIXME: instantiate one of each type of sensor for a Flo icd device
        sensor = FloRateSensor(self, flo_icd_id, json)
        self._hass_sensors.append( sensor )

        self.update_all_sensors()

    def get_waterflow_measurement(self, flo_icd_id):
        """Fetch latest state for a Flo inflow control device"""

        # request data for the last 30 minutes
        utc_timestamp = int(time.time()) - ( 60 * 30 )

        # FIXME: does API require from=? perhaps default behavior is better
        waterflow_url = '/waterflow/measurement/icd/' + flo_icd_id + '/last_day?from=' + utc_timestamp
        response = self._api_get_request(waterflow_url)
        # Response: [ {
        #               "average_flowrate": 0,
        #               "average_pressure": 86.0041294012751,
        #               "average_temperature": 68,
        #               "did": "606405bfe487",
        #               "total_flow": 0,
        #               "time": "2019-05-30T07:00:00.000Z"
        #             }, {}, ... ]
        json = response.json()

        # FIXME: return only the latest data point
        return json[0]

    def update_all_sensors(self):
        # for each Flo device, request the latest data for the last 30 minutes
        for sensor in self.hass_sensors():
            self._update()

    def hass_sensors(self):
        return self._hass_sensors

# FIXME:
# implement a separate sensor for each value vs attributes?
#  https://developers.home-assistant.io/docs/en/entity_sensor.html
#   e.g..  
#   device_class = temperature / unit_of_measurement = 'F'
#   device_class = ....    flow /  unit_of_measurement = 'gpm'
#   device_class = pressure /  unit_of_measurement = 'psi'

# pylint: disable=too-many-instance-attributes
class FloRateSensor(FloEntity):
    """Sensor for a Flo water inflow control device"""

    def __init__(self, flo_service, flo_icd_id, sensor_details_json):
        self._flo_icd_id = flo_icd_id
        self._sensor_details = sensor_details_json
        self._name = 'Flo ' + flo_icd_id
        self._state = '0'
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
        """Water flow rate for recent period"""
        return self._state

    @property
    def icon(self):
        """Icon for flow rate"""
        return 'mdi:water-pump'

    def update(self):
        """Update sensor state"""
        json = self._flo_service.get_waterflow_measurement(self._flo_icd_id)
        self._state = json['average_flowrate']
        self._attrs.update({
            ATTR_PRESSURE    : json['average_pressure'],
            ATTR_TEMPERATURE : json['average_temperature'],
            ATTR_TOTAL_FLOW  : json['total_flow']
        })