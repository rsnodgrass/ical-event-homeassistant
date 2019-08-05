"""
Remote interface to serial devices via IP2SL protocol
"""
import logging

import socket
import select

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.notify import (
    PLATFORM_SCHEMA, BaseNotificationService)
from homeassistant.const import (
    CONF_HOST, CONF_PORT)

log = logging.getLogger(__name__)

CONF_DATA = "data"
CONF_COMMANDS = "commands"
CONF_TIMEOUT = "timeout"
CONF_BUFFER_SIZE = "buffer_size"

DEFAULT_TIMEOUT = 0.250
DEFAULT_BUFFER_SIZE = 1024

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PORT): cv.port,
    vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
    vol.Required(CONF_COMMANDS): vol.All(
        cv.ensure_list,
        [
            {
                vol.Required(CONF_NAME): cv.string,
                vol.Required(CONF_DATA): cv.string,
            }
        ],
    ),
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup connections to IP2SL compatible devices"""

    devices = [ IP2SLRemote(host, port, commands, config) ]
    add_entities(devices, True)

class IP2SLRemote(remote.RemoteDevice):
    """Sends command to a remote serial connection exposed using IP2SL"""

    def __init__(self, host, port, commands, config):
        """Initialize device."""

        self._host = host
        self._port = port
        self._timeout = config.get(CONF_TIMEOUT, DEFAULT_TIMEOUT)
        self._buffersize = config.get(CONF_BUFFER_SIZE, DEFAULT_BUFFER_SIZE)
        self._commands = data.get(CONF_COMMANDS)

        # FIXME: need to determine if powered on; special key command/reply pattern to detect power?
        #        same with power on/off?
        self._power = False   
        self._name = 'IP2SL'

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._power

    def turn_on(self, **kwargs):
        """Turn the device on."""
        # FIXME: need to identify which is power on and power off from the command list!
        self._power = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the device off."""
        self._power = False
        self.schedule_update_ha_state()

    def update(self):
        """Update the device."""
        self.itachip2ir.update()

    def send_command(self, command, **kwargs):
        """Send multiple commands to an IP2SL compatible device."""
        for single_command in command:
            self.send_command(single_command)

    def send_command(self, command):
        """Send a command to an IP2SL compatible device"""

        # lookup the payload in the config
        payload = self._commands(command)
        if payload is None:
            log.error(f"Unknown command '{command}'; cannot send to {self._host} (port {self._port})")
            return

        payload = payload + '\r' # ensure CR always on end
        log.info(f"{command} --> payload: {payload}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(self._timeout)
            try:
                sock.connect((self._host, self._port))
                sock.send(payload.encode())

            except socket.error as err:
                log.error(f"Unable to send payload to {self._host} (port {self._port}): {err}")
                return

            input_ready, output_ready, exception = select.select(sock], [], [], self._timeout)
            if not input_ready:
                log.warning(f"Timeout after {self._timeout}s waiting for reply from {self._host}:{self._port}; sent '{payload}''")
                return
            else:
                value = sock.recv(self._buffersize).decode()
                log.info("Response: {}".format(value))

        return value