"""
Flo Smart Home Water Control System for Home Assistant
See https://github.com/rsnodgrass/hass-integrations/flo

For good example of update, see Leaf sensor/switch:
https://github.com/home-assistant/home-assistant/blob/dev/homeassistant/components/nissan_leaf/__init__.py

FUTURE APIS:
- https://api.meetflo.com/api/v1/icds/me
- https://api.meetflo.com/api/v1/alerts/icd/{flo_icd_id}?size=1
- https://api.meetflo.com/api/v1/alerts/icd/{flo_icd_id}?page=1&size=10
- https://api.meetflo.com/api/v1/locations/me
- https://api.meetflo.com/api/v1/users/me
- https://api.meetflo.com/api/v1/userdetails/me
"""
import logging
import json
import requests
import time
from threading import Thread, Lock

from homeassistant.helpers import discovery
from homeassistant.helpers.entity import Entity
from homeassistant.const import ( CONF_USERNAME, CONF_PASSWORD, CONF_NAME, CONF_SCAN_INTERVAL )
#from homeassistant.components.sensor import ( PLATFORM_SCHEMA )

_LOGGER = logging.getLogger(__name__)

FLO_DOMAIN = 'flo'
FLO_USER_AGENT = 'Home Assistant (Flo; https://github.com/rsnodgrass/hass-integrations/)'

# cache expiry in minutes; TODO: make this configurable (with a minimum to prevent DDoS)
FLO_CACHE_EXPIRY=10

FLO_UNIT_SYSTEMS = {
    'imperial_us': { 
        'system':   'imperial_us',
        'temp':     '°F',
        'flow':     'gpm',
        'pressure': 'psi',
    },
    'imperial_uk': { 
        'system':   'imperial_uk',
        'temp':     '°F',
        'flow':     'gpm',
        'pressure': 'psi',
    },
    'metric': { 
        'system':   'metric',
        'temp':     '°C',
        'flow':     'lpm',
        'pressure': 'kPa'
    }
}

mutex = Lock()

#CONFIG_SCHEMA = vol.Schema({
#    FLO_DOMAIN: vol.Schema({
#        vol.Required(CONF_USERNAME): cv.string,
#        vol.Required(CONF_PASSWORD): cv.string
#        vol.Optional(CONF_SCAN_INTERVAL, default=600): cv.positive_int
#    })
#}, extra=vol.ALLOW_EXTRA)

def setup(hass, config):
    """Set up the Flo Water Control System"""
#    conf = config[FLO_DOMAIN]
#    conf = {}
#    for component in ['sensor', 'switch']:
#        discovery.load_platform(hass, component, FLO_DOMAIN, conf, config)
    return True

class FloEntity(Entity):
    """Base Entity class for Flo water inflow control device"""

    def __init__(self, flo_service):
        """Store service upon init."""
        self._flo_service = flo_service
        self._attrs = {}

        if self._name is None:
            self._name = 'Flo Water' # default if unspecified

    @property
    def name(self):
        """Return the display name for this sensor"""
        return self._name

    @property
    def device_state_attributes(self):
        """Return the device state attributes."""
        return self._attrs

class FloService:
    """Client interface to the Flo service API"""

    def __init__(self, config):
        self._auth_token = None
        self._auth_token_expiry = 0
        
        self._username = config[CONF_USERNAME]
        self._password = config[CONF_PASSWORD]

        self._last_waterflow_measurement = None
        self._last_waterflow_update = 0

#        self._units = FLO_UNIT_SYSTEMS[self._get_unit_system]

    def _flo_authentication_token(self):
        now = int(time.time())
        if not self._auth_token or now > self._auth_token_expiry:
            # authenticate to the Flo API
            #   POST https://api.meetflo.com/api/v1/users/auth
            #   Payload: {username: "your@email.com", password: "1234"}

            auth_url = 'https://api.meetflo.com/api/v1/users/auth'
            payload = json.dumps({
                'username': self._username,
                'password': self._password
            })
            headers = { 
                'User-Agent': FLO_USER_AGENT,
                'Content-Type': 'application/json;charset=UTF-8'
            }

            _LOGGER.debug("Authenticating Flo account %s via %s", self._username, auth_url)
            response = requests.post(auth_url, data=payload, headers=headers)
            # Example response:
            # { "token": "caJhb.....",
            #   "tokenPayload": { "user": { "user_id": "9aab2ced-c495-4884-ac52-b63f3008b6c7", "email": "your@email.com"},
            #                     "timestamp": 1559246133 },
            #   "tokenExpiration": 86400,
            #   "timeNow": 1559226161 }

            json_response = response.json()

            _LOGGER.debug("Flo user %s authentication results %s : %s", self._username, auth_url, json_response)
            self._auth_token_expiry = now + int( int(json_response['tokenExpiration']) / 2)
            self._auth_token = json_response['token']

        return self._auth_token

    def get_request(self, url_path):
        url = 'https://api.meetflo.com/api/v1' + url_path
        headers = { 
            'authorization': self._flo_authentication_token(), 
            'User-Agent': FLO_USER_AGENT
        }
        response = requests.get(url, headers=headers)
        _LOGGER.debug("Flo GET %s : %s", url, response.content)
        return response

    def get_waterflow_measurement(self, flo_icd_id):
        """Fetch latest state for a Flo inflow control device"""

        # to avoid DDoS Flo's servers, cache any results loaded in last 10 minutes
        now = int(time.time())
        mutex.acquire()
        try:
            if self._last_waterflow_update > (now - (FLO_CACHE_EXPIRY * 60)):
                _LOGGER.debug("Using cached waterflow measurements (expiry %d min): %s",
                              FLO_CACHE_EXPIRY, self._last_waterflow_measurement)
                return self._last_waterflow_measurement
        finally:
            mutex.release()

        # request data for the last 30 minutes, plus Flo API takes ms since epoch
        timestamp = (now - ( 60 * 30 )) * 1000

        waterflow_url = '/waterflow/measurement/icd/' + flo_icd_id + '/last_day?from=' + str(timestamp)
        response = self.get_request(waterflow_url)
        # Example response: [ {
        #    "average_flowrate": 0,
        #    "average_pressure": 86.0041294012751,
        #    "average_temperature": 68,
        #    "did": "606405bfe487",
        #    "total_flow": 0,
        #    "time": "2019-05-30T07:00:00.000Z"
        #  }, {}, ... ]
        json_response = response.json()

        # Return the latest measurement data point. Strangely Flo's response list includes stubs
        # for timestamps in the future, so this searches for the last non-0.0 pressure entry
        # since the pressure always has a value even when the Flo valve is shut off.
        latest_measurement = json_response[0]
        for measurement in json_response:
            if measurement['average_pressure'] <= 0.0:
                continue

            if measurement['time'] > latest_measurement['time']:
                latest_measurement = measurement

        mutex.acquire()
        try:
            self._last_waterflow_measurement = latest_measurement
            self._last_waterflow_update = now
        finally:
            mutex.release()
    
        return latest_measurement

    def _get_unit_system(self):
        """Return user configuration, such as units"""

        response = self.get_request('/userdetails/me')
        # Example response: {
        #    "firstname": "Jenny",
        #    "lastname": "Tutone",
        #    "phone_mobile": "8008675309",
        #    "user_id": "7cab21-d488-3213-af31-c1ca20177b5a",
        #    "unit_system": "imperial_us"
        #  }
        json_response = response.json()
        return json_response['unit_system']
