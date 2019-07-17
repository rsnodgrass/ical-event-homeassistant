"""
Xantech Multi-Zone Amplifier Serial Controller
"""
import logging
import json
import requests

from homeassistant.const import ( CONF_HOST, CONF_PORT )

_LOGGER = logging.getLogger(__name__)

HASS_CONFIG_DOMAIN = 'xantech_mza'
CONF_MODULE = 'module'

CONFIG_SCHEMA = vol.Schema({
    HASS_CONFIG_DOMAIN: vol.Schema({
        vol.Optional(CONF_MODULE, default="xantech_mza"): cv.string,
        vol.Optional(CONF_HOST, default="localhost"): cv.string,
        vol.Optional(CONF_PORT, default=8888): cv.positive_int
    })
}, extra=vol.ALLOW_EXTRA)

def setup(hass, config):
    """Set up the Xantech Multi-Zone Amplifier integration"""

    # FIXME: support multiple instances of bridges (either modules or host/port/module tuples)
    service = XantechService( config[HASS_CONFIG_DOMAIN] )

    # dynamically create all the media players based on results 
    zone_details = service._get_request('/zones')
    for zone in zone_details['zones']:
        name = service.name() + " Zone " + zone        
#        discovery.load_platform(hass, 'media_player', FLO_DOMAIN, conf, config)
#        FIXME: inject name and service into each media player entity

    return True


class XantechService():
    """Client interface to the Xantech MZA microservice"""

    def __init__(self, config):
        self._host = config[CONF_HOST]
        self._port = config[CONF_PORT]
        self._module = config[CONF_MODULE]

        self._name = 'Xantech Audio'

        self._user_agent = 'Home Assistant (xantech_mza; https://github.com/rsnodgrass/hass-integrations/)'

    @property
    def name(self):
        return self._name

    @property
    def _base_url(self):
        """Returns the base URL for microservice endpoint"""
        return "http://" + self._host + ":" + str(self._port) + "/api/" + self._module)

    def _get_request(self, path=""):
        """Makes microservice GET request"""
        url = self._base_url + path
        headers = { 
            'User-Agent': self._user_agent
        }

        response = requests.get(url, headers=headers)
        _LOGGER.debug("GET %s : %s", url, response.content)
        return response.json()


    def _post_request(self, path="", d=""):
        """Makes microservice POST request and returns JSON parsed response"""
        url = self._base_url + path

        headers = { 
            'User-Agent': self._user_agent,
            'content-type': 'text/plain'
        }

        response = requests.post(url, data=str(d), headers=headers)
        _LOGGER.debug("POST %s %s: %s", url, data, response.content)
        return response.json()