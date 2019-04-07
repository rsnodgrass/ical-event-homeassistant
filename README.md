# iCal Status Sensor for Home Assistant

Sensor for Home Assistant that returns any currently scheduled event as the sensor status. If there
are multiple overlapping events, the most restrictive (shortest duration left) event is selected.

# Configuration

Example Home Assistant yaml sensor configuration, in this case it point to a calendar which contains
an event for each day of the week:

```
sensor:
- platform: ical_status
  name: "Day of the Week"
  url: "https://raw.githubusercontent.com/rsnodgrass/ical-status-homeassistant/master/examples/day-of-week.ics"
```

# Installation

Copy (ical_status/sensor.py) to config/custom_components/ical_status/sensor.py on your Home Assistant instance.

## Automatic Updates

For easy updateswhenever a new version is released, use the [Home Assistant custom_updater component](https://github.com/custom-components/custom_updater/wiki/Installation) and [Tracker card](https://github.com/custom-cards/tracker-card). Once those are setup, add the following custom_updater config:

``` 
custom_updater:
  track:
    - components
  component_urls:
    - https://raw.githubusercontent.com/rsnodgrass/ical-status-homeassistant/master/custom_updater.json
```

# Useful Examples

* a calendar of special days that trigger different light combinations (e.g. Valentine's Day)
* a calendar that returns the day of the week
* a calendar sensor which allows scheduling of triggers based on some calendar value



