"""
Main valve control for Flo Water Security System
"""
import logging

from homeassistant.components.switch import SwitchDevice, DOMAIN
from homeassistant.const import (CONF_DEVICES, CONF_HOST, CONF_MAC, CONF_NAME, CONF_ID)

_LOGGER = logging.getLogger(__name__)

# pylint: disable=unused-argument
async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Initialize the platform."""
    if discovery_info is None:
        return

class FloSwitch(SwitchDevice)
    """Representation of the control switch for Flo Water Security System."""

    def __init__(self, switch, data, mac):
        self._data = data
        self._name = switch[CONF_NAME]
        self._area_name = None
        if CONF_AREA_NAME in switch:
            self._area_name = switch[CONF_AREA_NAME]
            # if available, prepend area name to switch
            self._name = switch[CONF_AREA_NAME] + " " + switch[CONF_NAME]
        self._integration = int(switch[CONF_ID])
        self._is_on = False
        self._mac = mac

    async def async_added_to_hass(self):
        """Update initial state."""
        await self.query()

    async def query(self):
        """Query the Flo API for current status."""

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
        """Return the display name of this switch."""
        return self._name

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        attr = {ATTR_INTEGRATION_ID: self._integration}
        if self._area_name:
            attr[ATTR_AREA_NAME] = self._area_name
        return attr

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Instruct the switch to turn on."""

    async def async_turn_off(self, **kwargs):
        """Instruct the switch to turn off."""

    def update_state(self, value):
        """Update state."""
        self._is_on = value > 0

