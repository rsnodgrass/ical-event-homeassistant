"""
Support for Flo Water Security System

SWITCHES:
mode (home/away/sleep) ... not a switch
water status (on/off)
"""
import logging

from homeassistant.const import (
    CONF_USERNAME, CONF_PASSWORD, CONF_NAME, TEMP_FAHRENHEIT, STATE_ON, ATTR_TEMPERATURE
)
from . import FloEntity

_LOGGER = logging.getLogger(__name__)

# pylint: disable=unused-argument
def setup_platform(hass, config, add_switches_callback, discovery_info=None):
    """Setup the Flo Water Security System integration."""
    if discovery_info is None:
        return

    switches = []
    # FIXME: implement
    add_switches_callback(switches)

class FloControlSwitch(FloEntity, ToggleEntity):
    """Flo water inflow control device switch."""

    @property
    def name(self):
        """Switch name."""
        return "{} {}".format("Flo", "Water Control Valve")
   
    @property
    def is_on(self):
        """Return true if Flo control valve is on."""
        return False