# Xantech Control for Home Assistant

Support for Xantech multi-zone amplifiers for Home Assistant using the Xantech RS232 interface. This is compatible with the MRC88, MRAUDIO8X8 and possibly other Xantech amplifiers. Multiple Xantech amplifiers may be used and controlled simultaneously via a single Home Assistant interface.

Note that no plans exist to integrate or support Xantech mutli-zone room control pads. This is purely for allowing HA control of a Xantech multi-zone audio system.

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](YOUR_EMAIL_CODE)

## Installation

### Step 1: Install Custom Components

Copy all the files in [xantech/](https://github.com/rsnodgrass/hass-integrations/tree/master/xantech) GitHub directory to `/config/custom_components/xantech` on your Home Assistant installation.

```
__init__.py 
manifest.json
```

### Step 2: Configure Sensors

Example configuration:

```yaml
sensor:
  - platform: xantech
    tty: /dev/ttyXYZ
```

### Step 3: Add Lovelace Card

The following is a simplest Lovelace card which shows current state of Xantech zones:

```yaml
type: entities
entities:
  - entity: sensor.xantech_volume
```

![Flo Lovelace Examples](https://github.com/rsnodgrass/hass-integrations/blob/master/custom_components/flo/lovelace/entities.png?raw=true)

### Step 4: Configure Automatic Updates (optional)

This component support [HACS](https://github.com/custom-components/hacs) using the repository: rsnodgrass/hass-integrations

## See Also

* Xantech MRC88 RS332 Digital Interface manual

## Feature Requests

* subscribe to periodic and "zone change" status updates
* support basic audio settings per-zone
  - power on/off
  - volume + mute
  - source selection

No plans to implement:

* per-zone control of bass/treble/balance/etc

## Supported RS232

Zone Power On/Off
!{z#}PR{0/1}+ 

Input (Source) Select
!{z#}SS{s#}+ 
E.g. To set Zone 1 to Source Input 5: !1SS5+

Volume
!{z#}VO{v#}+ 

Volume Increment
!{z#}VI+ 

Volume Decrement
!{z#}VD+ 

Mute
!{z#}MU{0/1}+ 

Getting state:

Zone Activity Auto Update
!ZA{0/1}+ 

Zone Periodic Auto Update
!ZP{X seconds}+ 

Zone Data
?(z#}ZD+ 
Returns the status of the zone, minus the Metadata. 

## Hardware Interface Notes

The RS232 connector on the rear of the Xantech MRC88 and related controllers are wired such
that the Transmit and Receive lines already interchanged for direct communication with
a PC/RPi/etc using a standard RS232 serial cable (no Null Modem cable required).

The Xantech RS232 connector pin out is:

PIN # FUNCTION
1, 8, & 9 NC
2 Tx
3 Rx
4 DTR
5 GND
6 DSR
7 RTS
