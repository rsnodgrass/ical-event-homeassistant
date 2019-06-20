# Home Assistant Integrations

* [flo](custom_components/flo): support for the Flo water monitoring and control system

* [Hass.io Add-Ons](https://github.com/rsnodgrass/hassio-addons)

### Automatic Updates with Custom Updater (Optional)

For easy updates whenever new versions are released, use the [Home Assistant custom_updater component](https://github.com/custom-components/custom_updater/wiki/Installation) and [Tracker card](https://github.com/custom-cards/tracker-card). Once those are setup, add the following custom_updater config:

``` 
custom_updater:
  track:
    - components
  component_urls:
    - https://raw.githubusercontent.com/rsnodgrass/hass-integrations/master/custom_updater.json
```
