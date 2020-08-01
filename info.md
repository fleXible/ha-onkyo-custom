[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![](https://img.shields.io/badge/MAINTAINER-%40fleXible-red?style=flat)](https://github.com/fleXible)

# HomeAssistant - Onkyo Custom Component

This is a custom component to allow control of Onkyo, Integra and some recent Pioneer devices in 
[HomeAssistant](https://home-assistant.io).

This is a modified version of the built-in 
[onkyo](https://www.home-assistant.io/integrations/onkyo/) integration with these changes:

* All zones offered by onkyo device are disabled in HomeAssistent and won't show up as entities
* Populate state attributes when device is off
  * Fixes `Homekit` warning `"Sources out of sync. Restart Home Assistant"`
  * Set *"Hardware" - "Power Management" - "Network Standby"* to *"On"* for `source` property to be set correctly.
    If set to *"Off"*, last known value is used

## Configuration

Activate module by adding the line `onkyo_custom:` anywhere before your media_player config.

```yaml
# Example configuration.yaml entry
onkyo_custom:

media_player:
  - platform: onkyo_custom
    host: 192.168.1.2
    name: receiver
    sources:
      pc: 'HTPC'
```
 
For further documentation, consult the official HomeAssistant [onkyo](https://www.home-assistant.io/integrations/onkyo/) pages.
