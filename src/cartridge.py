import logging
import os.path


class CartridgeType(object):

    @staticmethod
    def get_description(cart_type):
        types_str = {
            0: 'ROM',

            # MBC1
            0x01: 'ROM+MBC1',
            0x02: 'ROM+MBC1+RAM',
            0x03: 'ROM+MBC1+RAM+BATT',

            # MBC2
            0x05: 'ROM+MBC2',
            0x06: 'ROM+MBC2+BATT',

            # ROM RAM
            0x08: 'ROM+RAM',
            0x09: 'ROM+RAM+BATTERY',

            # MMD1
            0x0B: 'ROM+MMD1',
            0x0C: 'ROM+MMD1+SRAM',
            0x0D: 'ROM+MMD1+SRAM+BATT',

            # MBC3
            0x0F: 'ROM+MBC3+TIMER+BATT',
            0x10: 'ROM+MBC3+TIMER+RAM+BATT',
            0x11: 'ROM+MBC3',
            0x12: 'ROM+MBC3+RAM',
            0x13: 'ROM+MBC3+RAM+BATT',

            # MBC5
            0x19: 'ROM+MBC5',
            0x1A: 'ROM+MBC5+RAM',
            0x1B: 'ROM+MBC5+RAM+BATT',
            0x1C: 'ROM+MBC5+RUMBLE',
            0x1D: 'ROM+MBC5+RUMBLE+SRAM',
            0x1E: 'ROM+MBC5+RUMBLE+SRAM+BATT',

            # Other
            0x1F: 'Pocket Camera',
            0xFD: 'Bandai TAMA5',

            # Hudson
            0xFE: 'Hudson HuC-3',
            0xFF: 'Hudson HuC-1',
        }

        return types_str[cart_type]

    @staticmethod
    def get_rom_size(rom_type):
        vals = {
            # Type( Rom size (bytes), banks)
            0x00: (32 * 1024, 2),
            0x01: (64 * 1024, 4),
            0x02: (128 * 1024, 8),
            0x03: (256 * 1024, 16),
            0x04: (512 * 1024, 32),
            0x05: (1024 * 1024, 64),
            0x06: (2048 * 2014, 128),
            0x52: (1152 * 1024, 72),
            0x53: (1280 * 1024, 80),
            0x54: (1536 * 1024, 96),
        }

        return vals[rom_type]

    @staticmethod
    def get_ram_size(ram_type):
        vals = {
            #type ( size, banks )
            0x00: (0, 0),
            0x01: (2 * 1024, 1),
            0x02: (8 * 1024, 1),
            0x03: (32 * 1024, 4),
            0x04: (128 * 1024, 16),
        }

        return vals[ram_type]


class Cartridge(object):

    def __init__(self, filename):
        self._filename = filename
        self._data = None
        self._log = logging.getLogger("Cartridge")

        self.is_loaded = self.load_cartridge(filename)
        if not self.is_loaded:
            return

        self.title = self._get_title()
        self.cartridge_type = self._data[0x147]
        self.cartridge_type_string = self._get_cartridge_type()

        self.designation = self._data[0x013F:0x0142].decode("utf-8")
        self.color_compatible = self._data[0x0143]

        # ROM specification - Size and bank number.
        self.rom_type = self._data[0x0148]
        self.rom_size, self.rom_banks = CartridgeType.get_rom_size(
            self.rom_type
        )

        # RAM specification - Size and bank number.
        self.ram_type = self._data[0x0149]
        self.ram_size, self.ram_banks = CartridgeType.get_ram_size(
            self.ram_type
        )

        self.destination = "JA" if self._data[0x14A] == 0 else "NA"
        self.rom_version = self._data[0x014C]
        self._log.debug(str(self))

    def __str__(self):
        output = "Rom variable summary:\n"
        for ele in self.__dict__:
            if ele == "_data":
                continue

            value = self.__dict__[ele]
            output += "[{}]: {}\n".format(ele, value)
        return output

    def load_cartridge(self, filename):
        log = self._log.getChild("load_cartridge")

        log.info("Filename: {}".format(filename))

        if not os.path.isfile(filename):
            log.error("Unable to load file [{}].".format(filename))
            return False

        with open(filename, 'rb') as handle:
            self._data = handle.read()
            log.info("Loaded {} bytes of data.".format(len(self._data)))

        return True

    def get_data(self):
        return self._data

    def _get_title(self):
        log = self._log.getChild("_get_title")

        # The title is up to 16 characters, and is \0 terminated.
        temp_title = self._data[0x134:0x142].partition(b'\0')[0].decode('utf-8')
        log.info("Loaded title: {}".format(temp_title))
        return temp_title

    def _get_cartridge_type(self):
        log = self._log.getChild("_get_cartridge_type")

        type_data = self._data[0x147]
        cart_type = CartridgeType.get_description(type_data)
        log.info("Cartridge type: {:02x} {}".format(type_data, cart_type))

        return cart_type
