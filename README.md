# iCal Status Sensor for Home Assistant

Sensor for Home Assistant that returns any currently scheduled event from a provided
iCal as the sensor status. If there are multiple overlapping events, the most
restrictive (shortest duration left) event is selected.

# Configuration

Example sensor configuration:

```
sensor:
  - platform: ical_status
    name: "Fun Days"
    url: "https://raw.githubusercontent.com/rsnodgrass/ical-status-homeassistant/master/examples/fundays.ics"
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
      entity_id: sensor.fun_days
      to: "St Patrick's Day"
    action:
      - service: lights.set_color
        data:
          entity_id: group.all_lights
          color: green
```

# Installation

Copy (ical_status/sensor.py) to config/custom_components/ical_status/ on your Home Assistant instance.

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

* sensor of special days that trigger different light combinations (e.g. Valentine's Day, St Patty's Day)
* sensor which allows scheduling of triggers based on some calendar value
* sensor schedule that returns the day of the week
* sensor schedule to trigger backups at various times during the week
* sensor schedule to only have triggers active during weekends
* sensor managed by your own Google calendar iCal feed
* sensor schedule based on AirBNB or rental occupancy calendar
* sensor schedule based on local community events

# See Also

* [iCal Validator](https://icalendar.org/validator.html)
* [Reoccuring Rule Generator](https://www.textmagic.com/free-tools/rrule-generator)
