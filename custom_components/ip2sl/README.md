# IP2SL for Home Assistant

***NOT IMPLEMENTED***

Exposes a [Remote](https://www.home-assistant.io/components/#remote) interface in Home Assistant
for one-way sending of commands to a serial connected device. No bi-directional
communication or response from remote commands is supported.

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

### Step 4: Configure Automatic Updates (optional)

This supports [HACS](https://github.com/custom-components/hacs) with the repository: rsnodgrass/hass-integrations

## TODO

* implement a more complex request/reply interaction model for complex interactions
* implement a serial sensor for IP2SL (see https://www.home-assistant.io/components/serial)
* implement support for local /dev/tty serial interfaces?
* implement sensors and binary sensor mappings as well (very complicated)

## See Also

* https://github.com/tinglis1/home-assistant-custom/tree/master/custom_components/notify

## Community Support

* https://community.home-assistant.io/t/itach-ip2sl/28805/10
