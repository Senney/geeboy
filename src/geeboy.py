import logging
from cartridge import Cartridge
from cpu import CPU
from instruction import OpcodeParser
from mem import mbc1
from screen import Screen


class GeeBoy(object):

    def __init__(self):
        # self.rom = "../data/loz.gb"
        # self.rom = "../data/test/individual/09-op r,r.gb"
        self.rom = "../test/simple-rom/simple.gb"

        self._cartridge = Cartridge(self.rom)

        self._codes = OpcodeParser()
        self._codes.load_instructions("./dat/opcodes.json")

        self._screen = Screen()

        self._mem = mbc1.MBC1(self._cartridge, self._screen)
        self._cpu = CPU(self._cartridge, self._mem, self._codes, self._screen)

        self._screen.set_cpu(self._cpu)
        self._cpu.run()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    gb = GeeBoy()
