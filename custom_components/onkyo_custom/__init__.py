"""The onkyo_custom component."""
import logging

import homeassistant.components.onkyo.media_player as onkyo_mp

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

    return True
