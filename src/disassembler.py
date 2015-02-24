from instruction import Instruction


class Disassembler(object):

    def __init__(self, cartridge, instr_set):
        self._cart = cartridge
        self._data = cartridge.get_data()
        self._codes = instr_set

    def _to_string(self, string, i):
        if "d8" in string:
            string = string.replace("d8", "{:02x}".format(self._data[i+1]))
        if "d16" in string:
            val = "{:02x}{:02x}".format(self._data[i+1], self._data[i+2])
            string = string.replace("d16", val)
        if "a16" in string:
            val = "{:02x}{:02x}".format(self._data[i+1], self._data[i+2])
            string = string.replace("a16", val)
        if "a8" in string:
            val = "0xFF00 + {:02x}".format(self._data[i+1])
            string = string.replace("a8", val)
        if "r8" in string:
            val = "SP + {:02x}".format(self._data[i+1])
            string = string.replace("r8", val)
        return string

    def disassemble(self, output):
        i = 0
        while i < len(self._data):
            op = int(self._data[i])
            if op == 0xCB:
                i += 1
                op = int(self._data[i])
                instr = self._codes.cb_instructions[op]
            else:
                instr = self._codes.instructions[op]

            if type(instr) is not Instruction:
                if 0x20 <= op <= 0x7E:
                    output.write("0x{:08x}: [{:02x}] {}\n"
                                 .format(i, op, chr(op)))
                else:
                    output.write("0x{:08x}: [{:02x}] ??\n"
                                 .format(i, op))

                i += 1
                continue

            output.write("0x{:08x}: [{:02x}] {}\n"
                         .format(i, op, self._to_string(str(instr), i)))
            i += instr.bytes
