"""
Exposes each zone of a Xantech multi-zone audio controllers/amplifiers as a Home Assistant media player entity.

FUTURE:
- auto-name zones based on dynamic results from microservice
- automatically create media player instances based on the configured zones on remote side (no need to configure each zone in YAML)

Inspired by Jesse Newland's mpr-6hmaut API
https://github.com/jnewland/ha-config/blob/master/custom_components/mpr_6zhmaut/media_player.py
"""
import logging
import requests
import voluptuous as vol

from homeassistant.const import (
    CONF_HOST, CONF_NAME, CONF_PORT, CONF_ZONE,
    STATE_OFF, STATE_ON)
from homeassistant.components.media_player import (
    MediaPlayerDevice, PLATFORM_SCHEMA)
from homeassistant.components.media_player.const import (
    SUPPORT_VOLUME_SET, SUPPORT_VOLUME_UP, SUPPORT_VOLUME_DOWN,
    SUPPORT_TURN_ON, SUPPORT_TURN_OFF,
    SUPPORT_VOLUME_MUTE, SUPPORT_SELECT_SOURCE)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.WARNING)

SUPPORT_MPR = SUPPORT_VOLUME_SET | SUPPORT_VOLUME_UP | SUPPORT_VOLUME_DOWN | \
              SUPPORT_VOLUME_MUTE | SUPPORT_SELECT_SOURCE | \
              SUPPORT_TURN_ON | SUPPORT_TURN_OFF

DOMAIN = 'xantech_mza'
CONF_PROTO = 'proto'
DEFAULT_PROTO = 'http'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PORT): cv.port,
    vol.optional(CONF_MODULE, default='xantech_mza'): cv.string,
    vol.Required(CONF_ZONE): cv.string,
    vol.Optional(CONF_PROTO, default=DEFAULT_PROTO): cv.string,
})

# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Initialize the multi-zone amplifier platform"""

    zone = AmplifierZone(
        config.get(CONF_NAME),
        config.get(CONF_HOST),
        config.get(CONF_PORT),
        config.get(CONF_MODULE),
        config.get(CONF_ZONE),
        config.get(CONF_PROTO),
    )
    if zone.update():
        add_devices([zone])
        return True
    else:
        return False

class AmplifierZone(MediaPlayerDevice):
    """Represents a single audio zone of the multi-zone amplifier"""

    # pylint: disable=too-many-public-methods
    def __init__(self, name, proto, host, port, module, zone):
        self._name = name

        self._proto = proto
        self._host = host
        self._port = port
        self._module = module

        self._zone = zone
        self._state_hash = {}

    @property
    def _base_url(self):
        """Returns the base URL for microservice endpoint"""
        # FIXME: modify the URL
        return self._proto + "://" + self._host + ":" + str(self._port) + "/api/xantech/zones/" + str(self._zone)

    def _request(self, method, path="", d=""):
        """Makes the actual request and returns the parsed response"""
        url = self._base_url + path

        if method == 'GET':
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, data=str(d), headers={'content-type': 'text/plain'})

        return response.json()

    def update(self):
        self._state_hash = self._request('GET')

        # FIXME: parse the response!

        if int(self._state_hash.get("zone")) != int(self._zone):
            return False

#        self._power_state = (int(self._state_hash.get("pr")) == 1)
#        self._volume = int(self._state_hash.get("vo")) / 38
#        self._muted = (int(self._state_hash.get("mu")) == 1)
#        self._source = self._state_hash.get("ch")

        return True

    @property
    def name(self):
        """Returns the name of the zone"""
        return self._name

    @property
    def state(self):
        """Returns the state of the zone"""
        if self._power_state:
            return STATE_ON

        return STATE_OFF

    @property
    def volume_level(self):
        """Volume level of the zone (range 0.0..1.0)"""
        return self._volume

    @property
    def is_volume_muted(self):
        """True if volume is currently muted"""
        return self._muted

    @property
    def media_title(self):
        """Current media source for the zone"""
        return self._source

    @property
    def supported_features(self):
        """Flags of media commands that are supported"""
        return SUPPORT_MPR

    @property
    def source(self):
        """"Return the current input source of the device"""
        return self._source

    @property
    def source_list(self):
        """List of available input sources"""
        # FIXME: this should discoverable...from endpoint (e.g. 4 zone units, 6 zone and 8 zone (and 12 for some)
        # FIXME: should these be optionally "named"? on microservice side
        return list(["1", "2", "3", "4", "5", "6", "7", "8"])

    def select_source(self, source):
        """ Set input source"""
        self._request("POST", "/source/" + str(source)), "")

    def turn_on(self):
        """Turn the zone media player on"""
        self._request("POST", "/power/on", "")

    def turn_off(self):
        """Turn the zone media player off"""
        self._request("POST", "/power/off", "")

    def set_volume_level(self, volume):
        """Set the volume level (range 0.0..1.0) """
        self._request("POST", "/volume/" + str(int(round(volume * 100))))

    def volume_up(self):
        """Increase the volume"""
        self._request("POST", "/volume/up", "")

    def volume_down(self):
        """Decrease the volume"""
        self._request("POST", "/volume/down", "")

    def mute_volume(self, mute):
        """Mute the media player"""
        if mute:
            self._request("POST", "/mute/on")
        else:
            self._request("POST", "/mute/off")
