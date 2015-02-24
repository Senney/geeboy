import logging
from cartridge import Cartridge
from disassembler import Disassembler
from instruction import OpcodeParser


class GeeBoy(object):

    def __init__(self):
        self._cartridge = Cartridge("../data/loz.gb")

        self._codes = OpcodeParser()
        self._codes.load_instructions("./dat/opcodes.json")

        self._disasm = Disassembler(self._cartridge, self._codes)
        handle = open("../data/loz.asm", "w")
        self._disasm.disassemble(handle)
        handle.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    gb = GeeBoy()
