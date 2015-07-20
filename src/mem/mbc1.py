import logging
from mem.memory import MemoryController


class MBC1(MemoryController):
    ROM_BANK_MODE = 0x0
    RAM_BANK_MODE = 0x1

    def __init__(self, cart, screen):
        super().__init__(cart, screen)
        self._log = logging.getLogger("MBC1")
        self.mode = self.ROM_BANK_MODE
        self.ram_enabled = True
        self.rom_bank = 1

        # Only define RAM if the cartridge actually has it.
        self.has_ram = self.cart.ram_type != 0x00
        self.ram_bank = 0
        if self.has_ram:
            self._emem = [0] * self.cart.ram_size

    def read(self, byte, size=1):
        if 0x0000 <= byte <= 0x3FFF:
            # Always read the 0'th bank of ROM data.
            return self._read_rom_data(byte, 0)
        if 0x4000 <= byte <= 0x7FFF:
            return self._read_rom_data(byte - 0x4000, self.rom_bank)
        if 0xA000 <= byte <= 0xBFFF:
            return self._read_external_memory(byte - 0xA000)

        return super().read(byte)

    def write(self, byte, value, size=1):

        # Writing to 0x0000-0x1FFF will enable or disable writing to the
        # cartridge RAM.
        if 0x0000 <= byte <= 0x1FFF:
            if value & 0xA == 0xA:
                self.ram_enabled = True
            else:
                self.ram_enabled = False
            return value

        # 0x2000 to 0x3FFF controls the ROM bank number.
        if 0x2000 <= byte <= 0x3FFF:
            self._select_rom_bank(value & 0x1F)
            return value

        if 0x4000 <= byte <= 0x5FFF:
            # See _change_memory_model to see what's going on here.
            if self.mode == self.ROM_BANK_MODE:
                self._select_rom_bank(self.rom_bank | (value & 0b11))
            else:
                self._select_ram_bank(value & 0b11)
            return value

        if 0x6000 <= byte <= 0x7FFF:
            self._change_memory_model(value)
            return value

        # External RAM.
        if 0xA000 <= byte <= 0xBFFF:
            if not self.ram_enabled:
                self._log.error("Attempted to write to RAM when RAM is not enabled.")
                return value

            return self._write_external_memory(byte, value)

        super().write(byte, value)

    def _change_memory_model(self, value):
        """
        Changes the "ROM/RAM Mode". The mode is either 0x0 (ROM_BANK_MODE)
        or 0x1 (RAM_BANK_MODE) which changes the 0x4000-0x5FFF memory region
        to control the bank number of either ROM or RAM.

        If the mode is set for ROM_BANK_MODE, the memory region mentioned
        above will represent the upper two bits of the ROM bank number.
        :param value:
        :return:
        """
        self.mode = value & 0x1
        self._log.debug("Setting memory model to: 0x{:02x}".format(value))
        return self.mode

    def _select_rom_bank(self, bank):
        """
        Selects the ROM bank to use in the 0x4000-0x7FFF memory region.
        Bank 0 is always mapped to 0x0000-0x3FFF (kinda like zero-page memory)
        :param bank:
        :return:
        """

        # 0x0 because we can't select the 0 bank,
        # the rest only occur when using the upper bits.
        if bank in [0x0, 0x20, 0x40, 0x60]:
            bank += 1
        self._log.debug("Setting ROM bank to: {}".format(bank))
        self.rom_bank = bank
        return self.rom_bank

    def _select_ram_bank(self, bank):
        """
        Selects the RAM bank that we're be using when we access the
        0xA000-0xBFFF region.

        In the MBC1 we can have up to 4 banks of memory (0x0-0x3).
        :param bank:
        :return:
        """
        if not self.has_ram:
            self._log.error("Attempted to select a RAM bank when no RAM is"
                            "installed in this cart.")
            self.ram_bank = 0
            return self.ram_bank
        if bank > 0x3:
            self._log.error("Attempted to set RAM bank out of the supported"
                            "range [0x0-0x3] [{}].".format(bank))
            self.ram_bank = 0
            return self.ram_bank

        # TODO: Check to see if the cart actually has this number of banks.

        self._log.debug("Setting RAM bank to: {}".format(bank))
        self.ram_bank = bank
        return self.ram_bank

    def _write_external_memory(self, byte, value):
        # The _emem buffer is the size of the entire possible buffer, we just simulate
        # bank switching by referencing further in to the array.
        # e.g. bank0 = 0x0000-0x1FFF
        #      bank1 = 0x2000-0x3FFF
        #      bank2 = 0x4000-0x5FFF
        #      bank3 = 0x6000-0x7FFF
        # For a total of 32 KB of addressable memory.
        region = 0x2000 * self.ram_bank
        memory_location = region + (byte - 0xA000)
        if memory_location > self.cart.ram_size:
            self._log.error("Attempted to write to RAM outside of the boundaries"
                            "of RAM [{:02x}]".format(byte))
            return value

        self._emem[memory_location] = value
        return value

    def _read_rom_data(self, byte, bank):
        """
        :param byte: The number of bytes offset in to the specified bank from
        which to read the data.
        :param bank: The bank from which to read.
        :return: The data at the ROM location.
        """
        region = 0x4000 * bank
        memory_location = region + byte
        if memory_location >= self.cart.rom_size:
            self._log.error("Attempted to read out of bounds of ROM.")
            return 0

        return self.cart.get_data()[memory_location]

    def _read_external_memory(self, offset):
        """
        Reads from the specified offset in to the external memory area.
        :param offset: The offset in to self._emem[]
        :return: The data at the specified offset in cartridge RAM.
        """
        region = 0x2000 * self.ram_bank
        memory_location = region + offset
        if memory_location >= self.cart.ram_size:
            self._log.error("Attempted to read out of bounds of RAM "
                            "[{:02x}]".format(offset))
            return 0

        return self._emem[memory_location]