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
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_OPEN_TILT | SUPPORT_CLOSE_TILT | SUPPORT_SET_TILT_POSITION | \
               SUPPORT_SET_POSITION | SUPPORT_OPEN | SUPPORT_CLOSE
    @property
    def is_closed(self):
        """Return the closed state. We define that as minimum sun passage."""
        return self._skylight.pos() == 100

    @property
    def is_opening(self):
        """Return true if the cover is opening."""
        return self._skylight.dir() < 0

    @property
    def is_closing(self):
        """Return true if the cover is closing."""
        return self._skylight.dir() > 0

    @property
    def current_cover_tilt_position(self):
        """Return current position of cover tilt.
        None is unknown, 0 is closed, 100 is fully open.
        """
        return int(100 - self._skylight.pos() / 2)

