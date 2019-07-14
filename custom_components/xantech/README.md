# Xantech Control for Home Assistant

Support for Xantech multi-zone amplifiers for Home Assistant using the Xantech RS232 interface. This is compatible with the MRC88 and other Xantech amplifiers. Multiple Xantech amplifiers may be used.

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](YOUR_EMAIL_CODE)

## Installation

### Step 1: Install Custom Components

Copy all the files in [xantech/](https://github.com/rsnodgrass/hass-integrations/tree/master/xantech) GitHub directory to `/config/custom_components/xantech` on your Home Assistant installation.

```
__init__.py 
manifest.json
```

### Step 2: Configure Sensors

Example configuration:

```yaml
sensor:
  - platform: xantech
    tty: /dev/ttyXYZ
```

### Step 3: Add Lovelace Card

The following is a simplest Lovelace card which shows current state of Xantech zones:

```yaml
type: entities
entities:
  - entity: sensor.xantech_volume
```

![Flo Lovelace Examples](https://github.com/rsnodgrass/hass-integrations/blob/master/custom_components/flo/lovelace/entities.png?raw=true)

### Step 4: Configure Automatic Updates (optional)

This component support [HACS](https://github.com/custom-components/hacs) using the repository: rsnodgrass/hass-integrations

## See Also

* Xantech MRC88 RS332 Digital Interface manual

## Feature Requests
