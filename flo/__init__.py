"""
Flo Smart Home Water Security System for Home Assistant
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

from homeassistant.helpers.entity import Entity
from homeassistant.const import ( CONF_USERNAME, CONF_PASSWORD, CONF_NAME )
#from homeassistant.components.sensor import ( PLATFORM_SCHEMA )

_LOGGER = logging.getLogger(__name__)

FLO_DOMAIN = 'flo'
FLO_COMPONENTS = [ 'sensor', 'switch' ]

#PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
#    vol.Required(CONF_USERNAME): cv.string,
#    vol.Required(CONF_PASSWORD): cv.string
#})

def setup(hass, config):
    """Set up the Flo Water Security System"""

    # FIXME: move the initial authentication to the server here
    # FIXME: we need to reauthenticate every N hours based on auth token details

#    for component in FLO_COMPONENTS:
#        load_platform(hass, component, FLO_DOMAIN, {}, flo_service)

    return True

class FloEntity(Entity):
    """Base Entity class for Flo water inflow control device"""

    def __init__(self, flo_service):
        """Store service upon init."""
        self._flo_service = flo_service
    
        if self._name is None:
            self._name = 'Flo Water' # default if unspecified

    @property
    def name(self):
        """Return the display name for this sensor"""
        return self._name

class FloService:
    """Client interface to the Flo service API"""

    def __init__(self, config):
        self._auth_token = None
        self._auth_token_expiry = 0
        
        self._username = config[CONF_USERNAME]
        self._password = config[CONF_PASSWORD]

    def _flo_authentication_token(self):
        now = int(time.time())
        if not self._auth_token or now > self._auth_token_expiry:
            # authenticate to the Flo API
            #   POST https://api.meetflo.com/api/v1/users/auth
            #   Payload: {username: "your@email.com", password: "1234"}
            _LOGGER.debug("Authenticating to Flo account %s", self._username)

            auth_url = 'https://api.meetflo.com/api/v1/users/auth'
            payload = {
                'username': self._username,
                'password': self._password
            }
            response = requests.post(auth_url, data=json.dumps(payload))
            # Example response:
            # { "token": "caJhb.....",
            #   "tokenPayload": { "user": { "user_id": "9aab2ced-c495-4884-ac52-b63f3008b6c7", "email": "your@email.com"},
            #                     "timestamp": 1559246133 },
            #   "tokenExpiration": 86400,
            #   "timeNow": 1559226161 }

            json_response = response.json()
            _LOGGER.debug("Flo user %s authenticated: %s", self._username, json)
            self._auth_token_expiry = now + int( int(json_response['tokenExpiration']) / 2)
            self._auth_token = json_response['token']

        return self._auth_token

    def get_request(self, url_path):
        url = 'https://api.meetflo.com/api/v1' + url_path
        response = requests.get(url, headers={ 'authorization': self._flo_authentication_token() })
        _LOGGER.info("Flo GET %s : %s", url, response.content)
        return response

    def get_waterflow_measurement(self, flo_icd_id):
        """Fetch latest state for a Flo inflow control device"""

        # request data for the last 30 minutes
        utc_timestamp = int(time.time()) - ( 60 * 30 )

        # FIXME: does API require from=? perhaps default behavior is better
        waterflow_url = '/waterflow/measurement/icd/' + flo_icd_id + '/last_day?from=' + utc_timestamp
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

        # FIXME: return only the latest data point
        return json_response[0]
