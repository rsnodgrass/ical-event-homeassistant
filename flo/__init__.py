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

from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, CONF_NAME
#from homeassistant.components.sensor import ( PLATFORM_SCHEMA )

_LOGGER = logging.getLogger(__name__)

FLO_DOMAIN = 'flo'
FLO_COMPONENTS = [ 'sensor', 'switch' ]

#PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
#    vol.Required(CONF_USERNAME): cv.string,
#    vol.Required(CONF_PASSWORD): cv.string,
#    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string
#})

def setup(hass, config):
    """Set up the Flo Water Security System"""

    # FIXME: move the initial authentication to the server here
    # FIXME: we need to possibly reauthenticate every N hours based on auth token details

    username = config[CONF_USERNAME]
    password = config[CONF_PASSWORD]

#    for component in FLO_COMPONENTS:
#        load_platform(hass, component, FLO_DOMAIN, {}, flo_icd_config)

    return True

class FloEntity(Entity):
    """Base Entity class for Flo water inflow control device"""

    def __init__(self, flo_service):
        """Store service upon init."""
        self._flo_service = flo_service

class FloService(config):
    """Client interface to the Flo service API"""

    def __init__(self, username, password):
        self._auth_token = None
        self._username = config[CONF_USERNAME]
        self._password = config[CONF_PASSWORD]

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
            # Example response:
            # { "token": "caJhb.....",
            #   "tokenPayload": { "user": { "user_id": "9aab2ced-c495-4884-ac52-b63f3008b6c7", "email": "your@email.com"},
            #                     "timestamp": 1559246133 },
            #   "tokenExpiration": 86400,
            #   "timeNow": 1559226161 }

            _LOGGER.debug("Flo authentication of %s received %s", self._username, response.json())
            self._auth_token = response.json()['token']

        return self._auth_token

    def get_request(self, url_path):
        headers = { 'authorization': self._flo_authentication_token() }
        url = 'https://api.meetflo.com/api/v1' + url_path
        response = requests.Request('GET', url, headers=headers).prepare()
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
        json = response.json()

        # FIXME: return only the latest data point
        return json[0]
