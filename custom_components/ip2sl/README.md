# IP2SL for Home Assistant

***NOT IMPLEMENTED; THIS IS JUST A THOUGHT EXPERIMENT AT THIS POINT***

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Exposes a very basic [Remote](https://www.home-assistant.io/components/#remote) interface in Home Assistant
for one-way sending of commands to a serial connected device. No bi-directional communication or response
from remote commands is supported.

This is handy, but not a subsitute for a real well defined set of Home Assistant interfaces to
control a given device. I’m not really convinced that a completely generic IP2SL interface fro
Home Assistant is useful except for initial experimentation. Amost every case I really ended up
spending time on, I want more discrete control over details (exact volume level, dimmer level
setting, passing source ids, etc)…or want the data/commands exposed in more complex interfaces
like media_player.

This is based on ideas from the [Home Assistant IP2SL notify implementation by tinglis1](https://github.com/tinglis1/home-assistant-custom/tree/master/custom_components/notify) and [iTach IR Remote](https://www.home-assistant.io/components/itach/).

#### Example

Examples calling the remote commands via HA service calls:

```
remote.send_command service: { "entity_id":"remote.amplifier", "command":"mute" }
```

```
remote.send_command service: { "entity_id":"remote.radiora", "command":"kitchen_light_on" }
```

#### Supported Devices

* Global Caché [iTach Flex](https://www.amazon.com/Global-Cache-iTach-Flex-IP/dp/B00C6FRPIC/), [iTach IP2SL](https://www.amazon.com/Global-Cache-iTach-Serial-IP2SL/dp/B0051BU1X4/), [iTach WF2SL](https://www.amazon.com/Global-Cache-iTach-Wi-Fi-Serial/dp/B0051BU42W/)
* [Virtual IP2SL](https://github.com/rsnodgrass/hassio-addons/tree/master/virtual-ip2sl) - supports wide variety of USB and other serial interfaces

## Configuring Automatic Updates (optional)

This supports [HACS](https://github.com/custom-components/hacs) with the repository: rsnodgrass/hass-integrations

## See Also

* https://github.com/tinglis1/home-assistant-custom/tree/master/custom_components/notify
* https://community.home-assistant.io/t/rs232-control-via-itach-ip2sl-tweak-of-itach-remote-component/117912/6

## Community Support

* https://community.home-assistant.io/t/itach-ip2sl/28805/10
