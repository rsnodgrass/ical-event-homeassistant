"""
Multi-Zone Control for Xantech Amplifiers for Home Assistant
See https://github.com/rsnodgrass/hass-integrations/custom_components_xantech
"""
import logging
from threading import Thread, Lock

from homeassistant.helpers import discovery
from homeassistant.helpers.entity import Entity
from homeassistant.const import ( CONF_NAME, CONF_SCAN_INTERVAL )

_LOGGER = logging.getLogger(__name__)

FLO_DOMAIN = 'xantech'

def setup(hass, config):
    """Set up the Xantech Multi-Zone Controller interface"""
    return True
