# Flo Water Sensor for Home Assistant

Support for [Flo Smart Home Water Security System](https://amzn.to/2WBn8tW?tag=rynoshark-20) for Home Assistant.

NOTE: This is a stub out only...and NOT yet implemented.

## Installation

### Step 1: Copy the scripts!

### Step 2: Initial Configuration

### Step 3: Add sensors to Home Assistant's configuration

Example configuration:

```yaml
sensor:
  - platform: flo
    username: your@email.com
    password: your_flo_password
```

### Step 5: Automatic Updates with Custom Updater (Optional)


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
* Buy [Flo by Moen](https://amzn.to/2WBn8tW?tag=rynoshark-20) Smart Home Water Security System
