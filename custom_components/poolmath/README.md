# Pool Math for Home Assistant

***NOT IMPLEMENTED; THIS IS JUST A THOUGHT EXPERIMENT AT THIS POINT***

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Creates sensors exposing the most recent test results for pools being tracked with Trouble Free Pools's [Pool Math](https://www.troublefreepool.com/blog/poolmath/) apps including [Pool Math iOS](https://apps.apple.com/us/app/pool-math-by-troublefreepool/id1228819359) and [Pool Math Android](https://play.google.com/store/apps/details?id=com.troublefreepool.poolmath&hl=en_US). 

Note: this **requires a PoolMath Premium subscription** for cloud access to your pools data.

Supports Pool Math test results:

• pH
* Free Chlorine (FC)
* Total Alkalinity (TA)
* Calcium Hardness (CH)
* Cyanuric Acid (CYA)
* Salt
* Borates

### Pool Math description from Trouble Free Pool:

From the [Trouble Free Pool](https://troublefreepool.com/) website:

"By following the TroubleFreePool method of caring for your pool, you will spend less time and money chasing crystal clear, algae free water, and more time lounging in the sun."
"Trouble Free Pool exists to develop and promote a simple, inexpensive, and effective system of pool care."
"Trouble Free Pool is a registered 501(c)3 non-profit who displays NO advertising on our site nor is our advice compromised by financial incentives. 

> PoolMath makes swimming pool care, maintenance and management easy by tracking chlorine, pH, alkalinity and other  levels to help calculate how much salt, bleach and other chemicals to add. 
> Crystal clear algae free pool water is what Trouble Free Pool Math is committed to. Pool Math performs all the calculations you need to keep your chlorine, pH, calcium, alkalinity, and stabilizer levels balanced. 


### Configuration

Under Settings of the Pool Math iOS or Android application, find the Sharing section.  Turn this on, which allows anyone with access to the unique URL to be able to view data about your pool. Your pool's URL will be displayed, use that in the YAML configuration for the poolmath sensor.

```yaml
sensor:
  - type: "poolmath"
    url: "https://troublefreepool.com/mypool/6WPG8yL"
```

## Automatic Updates (optional)

This supports [HACS](https://github.com/custom-components/hacs) with the repository: rsnodgrass/hass-integrations

## See Also

* [Trouble Free Pool PoolMath tool](https://www.troublefreepool.com/calc.html)
* [Pool Math iOS](https://apps.apple.com/us/app/pool-math-by-troublefreepool/id1228819359) 
* [Pool Math Android](https://play.google.com/store/apps/details?id=com.troublefreepool.poolmath&hl=en_US)
* [ABC's of Pool Water Chemistry by Trouble Free Pool](https://www.troublefreepool.com/blog/2018/12/12/abcs-of-pool-water-chemistry/)

## Community Support

* [How to use the Pool Math app?](https://www.troublefreepool.com/threads/how-to-use-the-pool-math-app.179282/)