"""
Support for Flo Water Control System inflow control device valve on/off switches

SWITCHES:
mode (home/away/sleep) ... not a switch
"""
import logging

from . import FloEntity

_LOGGER = logging.getLogger(__name__)

# pylint: disable=unused-argument
def setup_platform(hass, config, add_switches_callback, discovery_info=None):
    """Setup the Flo Water Control System integration."""

    switches = []
    switches.append( FloControlSwitch(None) ) # FIXME
    add_switches_callback(switches)

class FloControlSwitch(FloEntity, ToggleEntity):
    """Flo water inflow control device switch."""

    @property
    def name(self):
        """Inflow control valve switch name"""
        return "{} {}".format("Flo", "Water Control Valve") # FIXME
   
    @property
    def is_on(self):
        """Return true if Flo control valve is on."""
        return True # FIXME
