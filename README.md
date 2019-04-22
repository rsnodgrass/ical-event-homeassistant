# Home Assistant Integrations

* [ical_status](ical_status/): sensor state is based on current iCal calendar event titles

* [groupme](groupme/): sensor tracking new GroupMe messages being posted (DOES NOT WORK)

### Automatic Updates with Custom Updater (Optional)

For easy updates whenever new versions are released, use the [Home Assistant custom_updater component](https://github.com/custom-components/custom_updater/wiki/Installation) and [Tracker card](https://github.com/custom-cards/tracker-card). Once those are setup, add the following custom_updater config:

``` 
custom_updater:
  track:
    - components
  component_urls:
    - https://raw.githubusercontent.com/rsnodgrass/hass-integrations/master/custom_updater.json
```
