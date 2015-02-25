from mem.memory import *


class ROMOnly(MemoryController):

    def __init__(self, cart):
        super().__init__(cart)
        self._log = logging.getLogger("ROMOnly")
        self._log.info("Initialized 'ROMOnly' Memory Controller.")

    def read(self, byte, size=1):
        if byte < 0x00:
            raise MemoryOutOfBoundsError("ROM only requires that memory be "
                                         "within [0x0000, 0xFFFF].")
        if 0x0 < byte <= 0x7FFF:
            return self.cart.get_data()[byte]

        # The superclass will handle all generic memory accesses, such
        # as video ram, internal ram, etc.
        value = super().read(byte)
        if value is not None:
            return value

        raise MemoryOutOfBoundsError("Unable to read memory address [{:02x}]."
                                     .format(byte))

    def write(self, byte, value, size=1):
        if 0x0 < byte < 0x3FFF:
            raise MemoryOutOfBoundsError("Unable to write to BANK 0.")
        if 0x4000 < byte <= 0x7FFF:
            raise NotImplementedError("Bank switching is not implemented in ROM only.")

        value = super().write(byte, value)
        if value is not None:
            return value

        raise MemoryOutOfBoundsError("Unable to write memory address [{:02x}]"
                                     .format(byte))
