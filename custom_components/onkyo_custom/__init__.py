"""The onkyo_custom component."""
import logging

from homeassistant.components.onkyo.media_player import (
    DOMAIN,
    OnkyoDevice,
    OnkyoDeviceZone,
)
from homeassistant.const import STATE_ON

DATA_UPDATED = f"{DOMAIN}_data_updated"

_LOGGER = logging.getLogger(__name__)


def _refresh_current_source(self):
    is_device = "Pioneer Zone" not in self.name
    is_device and _LOGGER.debug("Updated source=%s for device=%s", self.source, self.entity_id)

    current_source = self._source_mapping[0]

    current_source_raw = self.command("input-selector query")
    if not current_source_raw:
        return

    # eiscp can return string or tuple. Make everything tuples.
    if isinstance(current_source_raw[1], str):
        current_source_tuples = (current_source_raw[0], (current_source_raw[1],))
    else:
        current_source_tuples = current_source_raw

    for source in current_source_tuples[1]:
        if source in self._source_mapping:
            current_source = self._source_mapping[source]
            break
        current_source = "_".join(current_source_tuples[1])

    self._current_source = current_source


async def async_added_to_hass(self):
    """Run when entity about to be added."""
    is_device = "Pioneer Zone" not in self.name
    is_device and _LOGGER.debug("Patched async_added_to_hass() called for device=%s", self.entity_id)

    if isinstance(self, OnkyoDeviceZone) or self.source is not None:
        return

    if self._source_mapping is not None:
        self.hass.helpers.dispatcher.async_dispatcher_connect(DOMAIN, self._refreh_current_source)


def state_attributes_wrapper(attribute):
    def state_attributes(self):
        """Return the state attributes."""
        is_device = "Pioneer Zone" not in self.name
        # is_device and _LOGGER.debug("Patched state_attributes() called")
        real_state = self.state
        self._pwstate = STATE_ON
        state_attr = attribute.fget(self)
        self._pwstate = real_state
        # is_device and _LOGGER.debug(f"state={self.state}, source={self.source}, state_attributes={state_attr}, name={self.name}")

        return state_attr

    return property(state_attributes, attribute.fset, attribute.fdel)


def select_source_wrapper(func):
    def select_source(self, source):
        is_device = "Pioneer Zone" not in self.name
        is_device and _LOGGER.debug(f"Patched select_source({source}) called, self.source={self.source}")
        result = func(self, source)
        is_device and _LOGGER.debug(f"self.source={self.source}")

        return result

    return select_source


async def async_setup(hass, config):
    """Set up the Onkyo Component."""
    OnkyoDevice.state_attributes = state_attributes_wrapper(OnkyoDevice.state_attributes)
    _LOGGER.debug("Patched class=OnkyoDevice, method=state_attributes sucessfully.")
    OnkyoDevice.select_source = select_source_wrapper(OnkyoDevice.select_source)
    _LOGGER.debug("Patched class=OnkyoDevice, method=select_source sucessfully.")
    # OnkyoDevice._refresh_current_source = _refresh_current_source
    # _LOGGER.debug("Patched class=OnkyoDevice, method=_refresh_current_source sucessfully.")
    # OnkyoDevice.async_added_to_hass = async_added_to_hass
    # _LOGGER.debug("Patched class=OnkyoDevice, method=async_added_to_hass sucessfully.")

    return True
