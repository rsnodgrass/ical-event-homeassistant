# iCal Status Sensor for Home Assistant

Sensor for Home Assistant that returns any currently scheduled event from a provided
iCal as the sensor status. If there are multiple overlapping events, the most
restrictive (shortest duration left) event is selected.

# Configuration

Example sensor configuration:

```
sensor:
  - platform: ical_status
    name: "Lighting Days"
    url: "https://raw.githubusercontent.com/rsnodgrass/hass-integrations/master/ical_status/examples/lighting-days.ics"
```

### Advanced:

Additional configurable entities:

```
   file: ...
   default: "Happy"
   fix_apple_format: True
```

### Example trigger based on a scheduled iCal event:

```
  - alias: "St Patrick's Day"
    trigger:
      platform: state
      entity_id: sensor.lighting_days
      to: "St Patrick's Day"
    action:
      - service: lights.set_color
        data:
          entity_id: group.all_lights
          color: green
```

# Installation

Copy (sensor.py) to config/custom_components/ical_status/ on your Home Assistant instance.

## Automatic Updates

For easy updates whenever a new version is released, use the [Home Assistant custom_updater component](https://github.com/custom-components/custom_updater/wiki/Installation) and [Tracker card](https://github.com/custom-cards/tracker-card). Once those are setup, add the following custom_updater config:

``` 
custom_updater:
  track:
    - components
  component_urls:
    - https://raw.githubusercontent.com/rsnodgrass/hass-integrations/master/custom_updater.json
```

# Useful Examples

* sensor of special days that trigger different light combinations (e.g. Valentine's Day, St Patty's Day)
* sensor for scheduling triggers based on a calendar state
* sensor schedule to trigger backups at various times during the week
* sensor schedule to only have triggers active during weekends
* sensor managed by your own Google calendar iCal feed
* sensor schedule based on AirBNB or rental occupancy calendar
* sensor schedule based on local community events
* sensor schedule based on reoccuring times (every 3rd Saturday at 8am)

# See Also

* [iCal Validator](https://icalendar.org/validator.html)
* [Reoccuring Rule Generator](https://www.textmagic.com/free-tools/rrule-generator)
