"""Support for Onkyo Receivers with some customizations."""
import logging

from homeassistant.components.media_player import ATTR_TO_PROPERTY
from homeassistant.components.onkyo.media_player import (
    OnkyoDevice,
    OnkyoDeviceZone,
    PLATFORM_SCHEMA as ONKYO_PLATFORM_SCHEMA,
    setup_platform as onkyo_setup_platform,
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = ONKYO_PLATFORM_SCHEMA


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Onkyo custom platform by calling original Onky `setup_platform()`."""
    _LOGGER.info('Setting up plattform=onkyo_custom')

    def super_add_entities(devices, update=False):
        """Helper function to transform devices to our customized code."""
        custom_devices = []

        for device in devices:
            original_class = device.__class__.__name__
            if original_class == 'OnkyoDeviceZone':
                _LOGGER.debug(f'Skipping transform for original_class={original_class}')
                custom_devices.append(device)
            else:
                custom_class = globals().get(f'Custom{original_class}')
                _LOGGER.debug(f'Transformed original_class={original_class} into custom_class={custom_class}')
                custom_devices.append(custom_class(device))

        _LOGGER.debug(f'Calling add_entities({custom_devices}, {update})')
        add_entities(custom_devices, update)

    onkyo_setup_platform(hass, config, super_add_entities, discovery_info)


class CustomOnkyoDevice(OnkyoDevice):
    """Representation of a customized Onkyo device."""

    # def __init__(
    #     self,
    #     receiver,
    #     sources,
    #     name=None,
    #     max_volume=SUPPORTED_MAX_VOLUME,
    #     receiver_max_volume=DEFAULT_RECEIVER_MAX_VOLUME,
    # ):
    #     """Initialize the Onkyo Receiver."""
    #     self._device = OnkyoDevice(receiver, sources, name, max_volume, receiver_max_volume)

    def __init__(self, onkyo_device):
        """Initialize the custom Onkyo Receiver."""
        self.__dict__.update(vars(onkyo_device))

    # def update(self):
    #     """Get the latest state from the device."""
    #     status = self.command("system-power query")
    #
    #     if not status:
    #         return
    #     if status[1] == "on":
    #         self._pwstate = STATE_ON
    #     else:
    #         self._pwstate = STATE_OFF
    #         return
    #
    #     volume_raw = self.command("volume query")
    #     mute_raw = self.command("audio-muting query")
    #     current_source_raw = self.command("input-selector query")
    #     hdmi_out_raw = self.command("hdmi-output-selector query")
    #     preset_raw = self.command("preset query")
    #     if not (volume_raw and mute_raw and current_source_raw):
    #         return
    #
    #     # eiscp can return string or tuple. Make everything tuples.
    #     if isinstance(current_source_raw[1], str):
    #         current_source_tuples = (current_source_raw[0], (current_source_raw[1],))
    #     else:
    #         current_source_tuples = current_source_raw
    #
    #     for source in current_source_tuples[1]:
    #         if source in self._source_mapping:
    #             self._current_source = self._source_mapping[source]
    #             break
    #         self._current_source = "_".join(current_source_tuples[1])
    #     if preset_raw and self._current_source.lower() == "radio":
    #         self._attributes[ATTR_PRESET] = preset_raw[1]
    #     elif ATTR_PRESET in self._attributes:
    #         del self._attributes[ATTR_PRESET]
    #
    #     self._muted = bool(mute_raw[1] == "on")
    #     #       AMP_VOL/MAX_RECEIVER_VOL*(MAX_VOL/100)
    #     self._volume = (
    #         volume_raw[1] / self._receiver_max_volume * (self._max_volume / 100)
    #     )
    #
    #     if not hdmi_out_raw:
    #         return
    #     self._attributes["video_out"] = ",".join(hdmi_out_raw[1])

    @property
    def state_attributes(self):
        """Return the state attributes."""
        state_attr = {
            attr: getattr(self, attr)
            for attr in ATTR_TO_PROPERTY
            if getattr(self, attr) is not None
        }

        return state_attr
