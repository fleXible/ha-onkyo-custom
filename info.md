[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![](https://img.shields.io/badge/MAINTAINER-%40fleXible-red?style=flat)](https://github.com/fleXible)

# HomeAssistant - Onkyo Custom Component

This is a custom component to allow control of Onkyo, Integra and some recent Pioneer devices in 
[HomeAssistant](https://home-assistant.io).

Is a modified version of the built-in 
[onkyo](https://www.home-assistant.io/integrations/onkyo/) integration:

* Configured devices are fully updated, even when the device is in `standby` mode, populating all attributes
* All available attributes are available, regardless of state to fix problems with `off` devices and `homekit`

## Configuration

Use `onkyo_custom` as platform for the media_player domain.

To add an Onkyo or Pioneer receiver to your installation, add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
media_player:
  - platform: onkyo_custom
    host: 192.168.1.2
    name: receiver
    sources:
      pc: 'HTPC'
```

 If your receiver has second or third zone’s available, they are displayed as additional media players with the same functionality as the main zone.
 
 For further documentation, consult the official HomeAssistant [onkyo](https://www.home-assistant.io/integrations/onkyo/) pages.

***
