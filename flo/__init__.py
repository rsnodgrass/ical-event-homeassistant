"""
Flo Smart Home Water Security System for Home Assistant
See https://github.com/rsnodgrass/hass-integrations/flo

For good example of update, see Leaf sensor/switch:
https://github.com/home-assistant/home-assistant/blob/dev/homeassistant/components/nissan_leaf/__init__.py
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

#    for component in FLO_COMPONENTS:
#        load_platform(hass, component, FLO_DOMAIN, {}, flo_icd_config)

    return True

class FloEntity(Entity):
    """Base Entity class for Flo water inflow control device"""

    def __init__(self, flo_service):
        """Store service upon init."""
        self._flo_service = flo_service