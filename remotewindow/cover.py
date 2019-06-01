"""
Support for solar sunroof opener

FIXME: allow specifying % to open
"""
import logging

_LOGGER = logging.getLogger(__name__)

# pylint: disable=unused-argument
def setup_platform(hass, config, add_covers_callback, discovery_info=None):
    covers = []
    add_covers_callback(covers)

class WindowCover(Entity):
    """Control for electronically openable window or skylight."""

    @property
    def name(self):
        """Window name"""
        return "Opening Window"
   
    @property
    def is_on(self):
        """Return true if is open."""
        return True # FIXME
