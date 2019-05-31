# Flo Water Sensor for Home Assistant

Support for [Flo Smart water monitoring and control device](https://amzn.to/2WBn8tW?tag=rynoshark-20) for Home Assistant. [Flo](https://meetflo.com) is typically installed on the main water supply line and has sensors for flow rate, pressure, and temperature as well as shut off capabilities. Water shut off can be done manually, remotely, as well as automatically by Flo's emergency monitoring service when a leak is detected.

### Supported Sensors

- water flow rate (gpm)
- water pressure (psi)
- water temperature (F)

## Installation

### Step 1: Copy the scripts!

```
mkdir /config/custom_components/flo
__init__.py 
sensor.py
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

### Step 3: Automatic Updates with Custom Updater (Optional)

For easy updates whenever a new version is released, use the [Home Assistant custom_updater component](https://github.com/custom-components/custom_updater/wiki/Installation) and [Tracker card](https://github.com/custom-cards/tracker-card). Once those are setup, add the following custom_updater config:

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

Ideas for future improvements:

- support on/off switch for main water supply
- support for the automated monitoring mode (home, away, sleep)
- support alerts like leaks detected
- support multiple Flo devices and locations within a single Home Assistant instance
- support triggering the system test of a Flo device
- support Flo's new data on the types of usage (e.g. toilets, etc)
