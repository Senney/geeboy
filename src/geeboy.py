import logging
from cartridge import Cartridge
from disassembler import Disassembler
from instruction import OpcodeParser
from mem import mbc1


class GeeBoy(object):

    def __init__(self):
        self._cartridge = Cartridge("../data/loz.gb")

        self._codes = OpcodeParser()
        self._codes.load_instructions("./dat/opcodes.json")

        self._mem = mbc1.MBC1(self._cartridge)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    gb = GeeBoy()
