# Xantech Multi-Zone Audio Control for Home Assistant

[Home Assistant](https://www.home-assistant.io/) support for Xantech multi-zone controllers and amplifiers that can be controlled via the Xantech's RS232 protocol using the [Xantech Multi-Zone Audio Serial Bridge](). This is compatible with the MRC88, MRAUDIO8X8 and possibly other Xantech amplifiers. Multiple Xantech amplifiers may be used and controlled simultaneously via a single Home Assistant interface.

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Installation

### Step 1: Install Custom Components

Copy all the files in [xantech_mza/](https://github.com/rsnodgrass/hass-integrations/tree/master/custom_components/xantech_mza) GitHub directory to `/config/custom_components/xantech_mza` on your Home Assistant installation.

```
__init__.py 
media_player.py
manifest.json
```

### Step 2: Configure Sensors

Example configuration:

```yaml
media_player:
  - platform: xantech_mza
    name: Living Room Speakers
    host: !secret xantech_bridge_ip
    port: !secret xantech_bridge_port
    zone: 1
  - platform: xantech_mza
    name: Bedroom Speakers
    host: !secret xantech_bridge_ip
    port: !secret xantech_bridge_port
    zone: 2
  - platform: xantech_mza
    name: Patio Speakers
    host: !secret xantech_bridge_ip
    port: !secret xantech_bridge_port
    zone: 3
```

Note that multiple Xantech audio controllers and zones can be simultaneously integrated by having
different instances of the remote microservice running.

### Step 3: Add Lovelace Card

The following is a simplest Lovelace card which shows current state of a Xantech zone:

```yaml
```

![Flo Lovelace Examples](https://github.com/rsnodgrass/hass-integrations/blob/master/custom_components/flo/lovelace/entities.png?raw=true)

### Step 4: Configure Automatic Updates (optional)

This component support [HACS](https://github.com/custom-components/hacs) using the repository: rsnodgrass/hass-integrations

# Future

* automatically configure all the media players for all zones based on dynamic configuration from microservice /api/xantech_mza/zones and /api/xantech_mza/sources.
* add support for named sources from microservice

## Unsupported

* No plans exist to integrate or support Xantech multi-zone room control pads (feel free to contribute).
