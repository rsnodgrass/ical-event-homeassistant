"""
Support for Flo Water Security System

SENSORS:
flowrate (gpm)
pressure (psi)
temp (F)
total_flow (cumulative for day)
last health test timestamp

SWITCHES:
mode (home/away/sleep)
water status (on/off)

FUTURE:
- convert to async
"""
import logging

from homeassistant.components.sensor import ( DOMAIN, PLATFORM_SCHEMA )
from homeassistant.const import (
    CONF_USERNAME, CONF_PASSWORD, CONF_NAME, TEMP_FAHRENHEIT, STATE_ON, ATTR_TEMPERATURE
)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

FLO_HASS_SLUG = 'flo'

ATTR_FLOWRATE   = 'flowrate'
ATTR_PRESSURE   = 'pressure'
ATTR_TOTAL_FLOW = 'total_flow'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string
})

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

#    hass.data[FLO_HASS_SLUG] = {}
#    hass.data[FLO_HASS_SLUG]['sensors'] = []
#    hass.data[FLO_HASS_SLUG]['sensors'].extend(sensors)

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

    def _flo_get_request(self, url_path):
        headers = { 'authorization': self._flo_authentication_token() }
        url = 'https://api.meetflo.com/api/v1' + url_path
        response = requests.Request('GET', url, headers=headers).prepare()
        _LOGGER.info("Flo GET %s : %s", url, response.content)
        return response

    def _initialize_sensors(self):
        response = self._flo_get_request('/icds/me')
        # Response: { "is_paired":true,
        #             "device_id":"a0b405bfe487",
        #             "id":"2faf8cd6-a8eb-4b63-bd1a-33298a26eca8",
        #             "location_id":"e7b2833a-f2cb-a4b1-ace2-36c21075d493" }
        json = response.json()
 
        # FIXME: *actually* support multiple devices (and locations)
        flo_icd_id = json['id']
        sensor = FloRateSensor(self, flo_icd_id, json)
        self._hass_sensors.append( sensor )

        self.update_all_sensors()

    def update_sensor(self, sensor):
        # request the latest data for the last 30 minutes
        utc_timestamp = int(time.time()) - ( 60 * 30 )

        # FIXME: does API require from=? perhaps default behavior is better
        waterflow_url = '/waterflow/measurement/icd/' + sensor.flo_id() + '/last_day?from=' + utc_timestamp
        response = self._flo_get_request(waterflow_url)
        # Response: [ {
        #               "average_flowrate": 0,
        #               "average_pressure": 86.0041294012751,
        #               "average_temperature": 68,
        #               "did": "606405bfe487",
        #               "total_flow": 0,
        #               "time": "2019-05-30T07:00:00.000Z"
        #             }, {}, ... ]
        json = response.json()
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
class FloRateSensor(Entity):
    """Sensor for a Flo Water Security System"""

    def __init__(self, flo_service, flo_icd_id, sensor_details_json):
        self._flow_service = flo_service
        self._flo_icd_id = flo_icd_id
        self._sensor_details = sensor_details_json
        self._name = 'Flo ' + flo_icd_id
        self._state = '0'

    @property
    def name(self):
        """Return the display name of this sensor"""
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
        json = self._flo_service.update_sensor(self)
        self._state = json['average_flowrate']
        self._attrs.update({
            ATTR_PRESSURE    : json['average_pressure'],
            ATTR_TEMPERATURE : json['average_temperature'],
            ATTR_TOTAL_FLOW  : json['total_flow']
        })