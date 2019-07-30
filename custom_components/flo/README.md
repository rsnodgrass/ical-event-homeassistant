# Flo Water Sensor for Home Assistant

Support for [Flo Smart water monitoring and control device](https://amzn.to/2WBn8tW?tag=rynoshark-20) for Home Assistant. [Flo](https://meetflo.com) is typically installed on the main water supply line and has sensors for flow rate, pressure, and temperature as well as shut off capabilities. Water shut off can be done manually, remotely, as well as automatically by Flo's emergency monitoring service when a leak is detected.

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

### Supported Sensors

- water flow rate (gpm)
- water pressure (psi)
- water temperature (&deg;F)

NOTE: Flo's webservice API only returns average sensor data for the previous 15 minute period.
Real-time sensor state is not available from Flo at this time.

## Installation

Visit the Home Assistant community if you need [help with installation and configuration of Flo](https://community.home-assistant.io/t/flo-smart-water-leak-detector/119532).

### Step 1: Install Flo Custom Components

Copy all the files in [flo/](https://github.com/rsnodgrass/hass-integrations/tree/master/flo) GitHub directory to `/config/custom_components/flo` on your Home Assistant installation.

```
__init__.py 
sensor.py
switch.py
manifest.json
```

### Step 2: Configure Sensors

Example configuration:

```yaml
sensor:
  - platform: flo
    username: your@email.com
    password: your_flo_password
```

### Step 3: Add Lovelace Card

The following is a simplest Lovelace card which shows data from the Flo sensors:

```yaml
type: entities
entities:
  - entity: sensor.flo_water_flow_rate
  - entity: sensor.flo_water_pressure
  - entity: sensor.flo_water_temperature
```

![Flo Lovelace Examples](https://github.com/rsnodgrass/hass-integrations/blob/master/custom_components/flo/lovelace/entities.png?raw=true)

Alternatively, Lovelace example with gauges that turn colors when pressure or flow rate is high:

```yaml
cards:
  - type: gauge
    name: Water Pressure
    entity: sensor.flo_water_pressure
    max: 100
    severity:
      green: 0
      yellow: 70
      red: 80
  - type: gauge
    name: Flow Rate
    entity: sensor.flo_water_flow_rate
    max: 15
    severity:
      green: 0
      yellow: 10
      red: 12
  - type: gauge
    name: Temp
    entity: sensor.flo_water_temperature
    max: 75
type: horizontal-stack
```

More complex cards can be created, for example the following shows both the basic entities card as well as a card built with mini-graph-card (see flo/lovelace/ folder for example cards):

![Flo Lovelace Examples](https://github.com/rsnodgrass/hass-integrations/blob/master/custom_components/flo/lovelace/mini-graph.png?raw=true)

### Step 4: Configure Automatic Updates (optional)

NOTE: This has been upgraded to support [HACS](https://github.com/custom-components/hacs) as well using the repository: rsnodgrass/hass-integrations

For easy updates whenever a new version is released, use the [Home Assistant custom_updater component](https://github.com/custom-components/custom_updater/wiki/Installation) and [Tracker card](https://github.com/custom-cards/tracker-card). Once those are setup, add the following custom_updater settings to your config:

```yaml
custom_updater:
  track:
    - components

  component_urls:
    - https://raw.githubusercontent.com/rsnodgrass/hass-integrations/master/flo/custom_updater.json
```

## See Also

* [Community support for Home Assistant Flo sensor](https://community.home-assistant.io/t/flo-smart-water-leak-detector/119532)
* [Check price of Flo water monitoring device on Amazon.com](https://amzn.to/2WBn8tW?tag=rynoshark-20)
* [Flo by Moen](https://meetflo.com) (official product page)
* [15% OFF purchases of Flo](https://meetflo.referralrock.com/l/818758/)

## Feature Requests

Priority improvements:

- support switching water supply on/off
- change to flo: domain configuration vs individual sensor (will be breaking change) to automatically create switches AND sensors (rather than having to configure independently)
- support changing the automatic water leak monitoring mode (home, away, sleep)
- support metric unit system (liter, C, kPa)
- auto-create a pressure sensor for status of water flow (Ok, Warning, Critical)

Other ideas (no plans to add currently):

- support Flo alerts (leaks detected)
- support multiple Flo devices and locations within a single Home Assistant instance
- support triggering the system test of a Flo device
- support Flo's fixtures beta feature breaking down usage by type (e.g. toilets, appliances, faucet, irrigation, etc)
- support leak detection sensitivity settings (all, small, bigger, biggest)
- create water sensor base class in Home Assistant (applies to other water sensing/shutoff valves)

## Automation Ideas

- automatically turn on Away mode for water control system when house goes into Away mode (and vice-a-versa)
- pre-warm heated towel rack when shower flow rate is detected
- toilet flush detection as an occupancy sensor (e.g. disable Away modes)

