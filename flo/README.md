# Flo Water Sensor for Home Assistant

Support for [Flo Smart water monitoring and control device](https://amzn.to/2WBn8tW?tag=rynoshark-20) for Home Assistant. [Flo](https://meetflo.com) is typically installed on the main water supply line and has sensors for flow rate, pressure, and temperature as well as shut off capabilities. Water shut off can be done manually, remotely, as well as automatically by Flo's emergency monitoring service when a leak is detected.

### Supported Sensors

- water flow rate (gpm)
- water pressure (psi)
- water temperature (&deg;F)

NOTE: Flo's webservice API only returns average sensor data for the previous 15 minute period.
Real-time sensor state is not available from Flo at this time.

## Installation

Visit the Home Assistant community if you need [help with installation and configuration of Flo](https://community.home-assistant.io/t/flo-water-sensor/10160/149).

### Step 1: Install Flo Custom Components

Copy all the files in [flo/](https://github.com/rsnodgrass/hass-integrations/tree/master/flo) Github directory to `/config/custom_components/flo` on your Home Assistant installation.

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

More complex cards can be created, for example the following shows both the basic entities card as well as a card build with mini-graph-card:

![Flo Lovelace Examples](https://github.com/rsnodgrass/hass-integrations/blob/master/flo/lovelace/flo-lovelace-examples.png?raw=true)

### Step 4: Configure Automatic Updates (optional)

For easy updates whenever a new version is released, use the [Home Assistant custom_updater component](https://github.com/custom-components/custom_updater/wiki/Installation) and [Tracker card](https://github.com/custom-cards/tracker-card). Once those are setup, add the following custom_updater settings to your config:

```yaml
custom_updater:
  track:
    - components

  component_urls:
    - https://raw.githubusercontent.com/rsnodgrass/hass-integrations/master/custom_updater.json
```

## See Also

* [Community support for Home Assistant Flo sensor](https://community.home-assistant.io/t/flo-water-sensor/10160/149)
* [Check price of Flo water monitoring device on Amazon.com](https://amzn.to/2WBn8tW?tag=rynoshark-20)
* [Flo by Moen](https://meetflo.com) (official product page)

## Feature Requests

Priority improvements:

- support for switching water supply on/off
- support for changing the automatic monitoring mode (home, away, sleep)
- support imperial_us (gpm, F, psi) vs metric unit system (liter, C, kPa)

Other ideas (no plans to add currently):

- support Flo alerts (leaks detected)
- support multiple Flo devices and locations within a single Home Assistant instance
- support triggering the system test of a Flo device
- support Flo's new fixtures beta features breaking down types of usage (e.g. toilets, appliances, faucet, irrigation, etc)
