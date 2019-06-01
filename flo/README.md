# Flo Water Sensor for Home Assistant

Support for [Flo Smart water monitoring and control device](https://amzn.to/2WBn8tW?tag=rynoshark-20) for Home Assistant. [Flo](https://meetflo.com) is typically installed on the main water supply line and has sensors for flow rate, pressure, and temperature as well as shut off capabilities. Water shut off can be done manually, remotely, as well as automatically by Flo's emergency monitoring service when a leak is detected.

### Supported Sensors

- water flow rate (gpm)
- water pressure (psi)
- water temperature (F)

## Installation

Visit the Home Assistant community if you need [help with installation and configuration of Flo](https://community.home-assistant.io/t/flo-water-sensor/10160/149).

### Step 1: Copy the scripts!

Copy all the files in flo/ to /config/custom_components/flo on your Home Assistant installation.

```
__init__.py 
sensor.py
switch.py
manifest.json
```

### Step 2: Add sensors to Home Assistant's configuration

Example configuration:

```yaml
sensor:
  - platform: flo
    username: your@email.com
    password: your_flo_password
```

### Step 3: Automatic Updates (Optional)

For easy updates whenever a new version is released, use the [Home Assistant custom_updater component](https://github.com/custom-components/custom_updater/wiki/Installation) and [Tracker card](https://github.com/custom-cards/tracker-card). Once those are setup, add the following custom_updater settings to your config:

```yaml
custom_updater:
  track:
    - components

  component_urls:
    - https://raw.githubusercontent.com/rsnodgrass/hass-integrations/master/custom_updater.json
```

## See Also

* https://community.home-assistant.io/t/flo-water-sensor/10160/149
* [Check price of Flo water monitoring system on Amazon.com](https://amzn.to/2WBn8tW?tag=rynoshark-20)
* [Flo by Moen](https://meetflo.com)

## Future Improvements

Priority improvements:

- support for switching water supply on/off
- support for changing the automatic monitoring mode (home, away, sleep)

Ideas for future improvements (no plans to add currently):

- support Flo alerts (leaks detected)
- support multiple Flo devices and locations within a single Home Assistant instance
- support triggering the system test of a Flo device
- support Flo's new fixtures beta features breaking down types of usage (e.g. toilets, appliances, faucet, irrigation, etc)
