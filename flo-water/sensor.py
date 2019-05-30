"""
Sensor for Flo Water Security System

SENSORS:
flow (gpm)
pressure (psi)
temp (F)
last health test timestamp

SWITCHES:
mode (home/away/sleep)
water status (on/off)
"""
import logging

from homeassistant.components.sensor import DOMAIN
from homeassistant.const import (CONF_DEVICES, CONF_HOST, CONF_MAC,
                                 CONF_NAME, CONF_ID)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

# pylint: disable=unused-argument
async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Setup the platform."""
    if discovery_info is None:
        return

# pylint: disable=too-many-instance-attributes
class FloSensor(Entity):
    """Representation of a Flo Water Security System."""

    def __init__(self, data):
        self._data = data
        self._area_name = None

    @property
    def integration(self):
        """Return the Integration ID."""
        return self._integration

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        if self._mac is not None:
            return "{}_{}_{}_{}".format(COMPONENT_DOMAIN,
                                        DOMAIN, self._mac,
                                        self._integration)
        return None

    @property
    def name(self):
        """Return the display name of this sensor."""
        return self._name

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        attr = {ATTR_INTEGRATION_ID: self._integration}
        if self._area_name:
            attr[ATTR_AREA_NAME] = self._area_name
        return attr

    @property
    def state(self):
        """State of the device."""
        return self._state

    def update_state(self, state):
        """Update state."""
        self._state = state
