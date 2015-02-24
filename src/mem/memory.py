import logging
from cartridge import Cartridge


class MemoryOutOfBoundsError(Exception):
    pass


class MemoryAccessDeniedError(Exception):
    pass


class MemoryController(object):

    def __init__(self, cart):
        """
        :type cart: Cartridge
        """
        self.type = "GenericMemoryUnit"
        self.cart = cart
        self._log = logging.getLogger("MemoryController")

        # Video RAM
        self._video = [0]*(0xA000-0x8000)

        # External and Internal memory
        self._emem = None
        self._imem = [0]*(0xE000-0xC000)
        self._hmem = [0]*(0xFFFF-0xFF80)

        # Object Attribute Memory
        # Stores attributes for each of the sprites being drawn on the screen.
        self._oam = [0]*(0xFEA0-0xFE00)

        # Hardware Registers
        self._hreg = [0]*(0xFF80-0xFF00)

        # Interrupt Enable Register
        self.interrupts_enabled = True

    def read(self, byte, size=1):
        """
        Generic read which will read from any of the Gameboy's memory units.
        :type byte int
        :type size int
        :param byte: The byte to read.
        :param size: The number of bytes to read. Currently not implemented.
        :return:
        """

        # Video Memory
        if 0x8000 <= byte <= 0x9FFF:
            return self._video[byte-0x8000]

        # Internal Memory
        if 0xC000 <= byte <= 0xDFFF:
            return self._imem[byte-0xC000]

        # Reserved Memory
        if 0xE000 <= byte <= 0xFDFF:
            self._log.warning("Nintendo standards specify that reading from "
                              "[E000-FDFF] is discouraged.")
            return self._imem[(byte-0xE000)]

        # Unused Memory
        if 0xFEA0 <= byte <= 0xFEFF:
            raise MemoryAccessDeniedError("Attempted to read from unused RAM"
                                          " space.")

        # Hardware Registers
        if 0xFF00 <= byte <= 0xFF7F:
            return self._hreg[byte - 0xFF00]

        # High memory
        if 0xFF80 <= byte <= 0xFFFE:
            return self._hmem[byte - 0xFF80]

        # Interrupt Enabled register
        if byte == 0xFFFF:
            return self.interrupts_enabled

    def write(self, byte, value, size=1):
        raise NotImplementedError("Cannot write. No ROM or RAM defined.")

    def check_bit(self, byte, bit):
        mask = 1 << bit
        value = self.read(byte) & mask
        return value == 1

    def set_bit(self, byte, bit, value):
        mask = 1 << bit
        current = self.read(byte)
        current &= ~mask
        if value:
            current |= mask
        self.write(byte, current)
        return current


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


class MBC1(MemoryController):

    def __init__(self, cart):
        super().__init__(cart)

    def read(self, byte, size=1):
        pass

    def write(self, byte, value, size=1):
        pass

