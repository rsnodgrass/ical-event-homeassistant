# IP2SL for Home Assistant

***NOT IMPLEMENTED; THIS IS JUST A THOUGHT EXPERIMENT AT THIS POINT***

Exposes a [Remote](https://www.home-assistant.io/components/#remote) interface in Home Assistant
for one-way sending of commands to a serial connected device. No bi-directional
communication or response from remote commands is supported.

I’m not really convinced that a completely generic IP2SL interface from Home Assistant is useful except for initial experimentation. Amost every case I get into, I want more discrete control over details (exact volume level, dimmer level setting, passing source ids, etc)…or want the data/commands exposed in more complex interfaces like media_player.

This is based on ideas from the [Home Assistant IP2SL notify implementation by tinglis1](https://github.com/tinglis1/home-assistant-custom/tree/master/custom_components/notify) and [iTach IR Remote](https://www.home-assistant.io/components/itach/).

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
* https://community.home-assistant.io/t/rs232-control-via-itach-ip2sl-tweak-of-itach-remote-component/117912/6

## Community Support

* https://community.home-assistant.io/t/itach-ip2sl/28805/10
