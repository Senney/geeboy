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
            val = self._imem[byte-0xC000]
            return val

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
            return 1 if self.interrupts_enabled else 0

        return 0xFF

    def write(self, byte, value, size=1):
        # Video Memory
        if 0x8000 <= byte <= 0x9FFF:
            self._video[byte-0x8000] = value

        # Internal Memory
        if 0xC000 <= byte <= 0xDFFF:
            self._imem[byte-0xC000] = value

        # Reserved Memory
        if 0xE000 <= byte <= 0xFDFF:
            raise MemoryAccessDeniedError("Cannot write to ECHO RAM")

        # Unused Memory
        if 0xFEA0 <= byte <= 0xFEFF:
            raise MemoryAccessDeniedError("Cannot write to Unused Memory")

        # Hardware Registers
        if 0xFF00 <= byte <= 0xFF7F:
            raise NotImplementedError("Hardware registers are not implemented yet.")

        # High memory
        if 0xFF80 <= byte <= 0xFFFE:
            self._hmem[byte - 0xFF80] = value

        # Interrupt Enabled register
        if byte == 0xFFFF:
            self.interrupts_enabled = 1 if value == 0x1 else 0

        return None

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