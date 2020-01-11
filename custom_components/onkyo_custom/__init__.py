"""The onkyo_custom component."""


# class Test:
#     def __init__(self, attr1, attr2):
#         self._attr1 = attr1
#         self._attr2 = attr2
#
#     @property
#     def attr1(self):
#         print("Test.attr1")
#         return self._attr1
#
#     @property
#     def attr2(self):
#         print("Test.attr2")
#         return self._attr2
#
#
# class CustomOnkyoDevice(Test):
#     """Representation of a customized Onkyo device."""
#
#     # def __init__(
#     #     self,
#     #     receiver,
#     #     sources,
#     #     name=None,
#     #     max_volume=SUPPORTED_MAX_VOLUME,
#     #     receiver_max_volume=DEFAULT_RECEIVER_MAX_VOLUME,
#     # ):
#     #     """Initialize the Onkyo Receiver."""
#     #     self._device = OnkyoDevice(receiver, sources, name, max_volume, receiver_max_volume)
#
#     def __init__(self, onkyo_device):
#         """Initialize the custom Onkyo Receiver."""
#         self.__dict__.update(vars(onkyo_device))
#         #self._device = onkyo_device
#
#     #def __getattr__(self, name):
#     #    print("CustomOnkyoDevice.__getattr__(%s)" % name)
#     #    #return getattr(self._device, name)
#
#     #def __setattr__(self, name, value):
#     #    print("Attempt to edit the attribute %s" % name)
#     #    # return nx.Graph.__setattr__(self, attr, value)
