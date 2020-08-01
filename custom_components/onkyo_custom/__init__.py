"""The onkyo_custom component."""
import logging

import homeassistant.components.onkyo.media_player as onkyo_mp
from homeassistant.const import STATE_OFF, STATE_ON

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """Set up onkyo_custom integration."""

    def determine_zones(receiver):
        """Report all zones as disabled."""
        return {"zone2": False, "zone3": False}

    onkyo_mp.determine_zones = determine_zones
    _LOGGER.debug(
        'Patched <function determine_zones, file "%s"> with %s',
        __file__,
        determine_zones.__code__,
    )

    @property
    def last_source(self):
        """Return the last known input source of the device."""
        return self._last_source

    setattr(onkyo_mp.OnkyoDevice, "_last_source", None)
    onkyo_mp.OnkyoDevice.last_source = last_source
    _LOGGER.debug(
        'Added <property OnkyoDevice.last_source, file "%s"> from %s',
        __file__,
        last_source.fget.__code__,
    )

    def refresh_current_source(self) -> None:
        """Get current selected source from the device or the last active source."""
        current_source_raw = self.command("input-selector query")
        if not current_source_raw:
            self._current_source = self.last_source
            _LOGGER.debug(
                "Updated source=%s for entity_id=%s from last_source",
                self.source,
                self.entity_id,
            )
            return

        # eiscp can return string or tuple. Make everything tuples.
        if isinstance(current_source_raw[1], str):
            current_source_tuples = (current_source_raw[0], (current_source_raw[1],))
        else:
            current_source_tuples = current_source_raw

        for source in current_source_tuples[1]:
            if self._source_mapping and source in self._source_mapping:
                self._current_source = self._source_mapping[source]
                break
            self._current_source = "_".join(current_source_tuples[1])
        _LOGGER.debug(
            "Updated source=%s for entity_id=%s from device",
            self.source,
            self.entity_id,
        )

    onkyo_mp.OnkyoDevice.refresh_current_source = refresh_current_source
    _LOGGER.debug(
        'Patched <function OnkyoDevice.refresh_current_source, file "%s"> with %s',
        __file__,
        refresh_current_source.__code__,
    )

    def state_attributes(attribute):
        def wrapper(self):
            """Return the state attributes."""
            current_state = self.state
            if current_state is STATE_OFF:
                self._pwstate = STATE_ON

            state_attr = attribute.fget(self)

            if current_state is STATE_OFF:
                self._pwstate = current_state
                _LOGGER.debug(
                    f"state_attributes: name={self.name}, state={self.state}, "
                    f"source={self.source}, state_attributes={state_attr}"
                )

            return state_attr

        return property(wrapper, attribute.fset, attribute.fdel)

    onkyo_mp.OnkyoDevice.state_attributes = state_attributes(
        onkyo_mp.OnkyoDevice.state_attributes
    )
    _LOGGER.debug(
        'Patched <function OnkyoDevice.state_attributes, file "%s"> with %s',
        __file__,
        state_attributes.__code__,
    )

    def update(original_update):
        """Monkey patch `update` method, to always populate attributes in state.

        The attributes are only populated by `media_player` component, when `state` is on.
        This function applies a monkey-patch to always populate them, because otherwise `Homekit`
        will show warning "Sources out of sync. Restart Home Assistant"

        The setting "Hardware" - "Power Management" - "Network Standby" has to be "On" for
        the `source` property to be set correctly. Otherwise the last active source will the used.
        """

        def wrapper(self):
            """Get the latest state from the device."""
            if self.entity_id is None:
                return

            original_update(self)

            if self.state is STATE_OFF and self.source is None:
                self.refresh_current_source()
                _LOGGER.debug(
                    "update: entity_id=%s, source=%s", self.entity_id, self.source,
                )
            elif self.last_source != self.source:
                self._last_source = self.source
                _LOGGER.debug(
                    "update: entity_id=%s, last_source=%s",
                    self.entity_id,
                    self.last_source,
                )

        return wrapper

    onkyo_mp.OnkyoDevice.update = update(onkyo_mp.OnkyoDevice.update)
    _LOGGER.debug(
        'Patched <function OnkyoDevice.state_attributes, file "%s"> with %s',
        __file__,
        state_attributes.__code__,
    )

    return True
