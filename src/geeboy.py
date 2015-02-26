import logging
from cartridge import Cartridge
from cpu import CPU
from disassembler import Disassembler
from instruction import OpcodeParser
from mem import mbc1


class GeeBoy(object):

    def __init__(self):
        self._cartridge = Cartridge("../data/loz.gb")

        self._codes = OpcodeParser()
        self._codes.load_instructions("./dat/opcodes.json")

        self._mem = mbc1.MBC1(self._cartridge)
        self._cpu = CPU(self._cartridge, self._mem, self._codes)
        self._cpu.run()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    gb = GeeBoy()
