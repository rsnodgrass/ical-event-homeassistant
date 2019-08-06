# GroupMe Message Sensor for Home Assistant

***IMPLEMENTATION NOT WORKING YET***

Sensor for Home Assistant that returns true if any 'recent' messages
match a set of provided patterns. This uses the
[GroupMe API](https://dev.groupme.com).


Use case: this monitors a whale watching GroupMe group for new messages
to raise the sensor when whales have been sighted in a certain area.

# Configuration

Example sensor configuration:

```
sensor:
  - platform: groupme
    name: "Whale Watch"
    keywords: [ "orcas", "lopez" ]
```

### Example trigger:

```
  - alias: "Whales Sighted"
    trigger:
      platform: state
      entity_id: sensor.groupme_whale_watch
      to: 'on'
    action:
      - service: notify.notify
        data_template:
          message: "Whale's sighted!"
```

# Installation

Copy (groupme/sensor.py) to config/custom_components/groupme/ on your Home Assistant instance.

## Setup GroupMe Developer App

You must create an application on https://dev.groupme.com/applications/new

* Application Name: Home Assistant
* Callback URL: https://youroathurl/
* Developer Company: Personal
* Developer Address: N/A

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

* monitor a whale watching GroupMe group for new favorited messages which indicates whales have been sighted

# See Also

* [GroupMe API](https://dev.groupme.com)
* [GroupyAPI Python API](https://pypi.org/project/GroupyAPI/)
