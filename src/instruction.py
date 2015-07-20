import json
import os.path
import logging


class Instruction(object):
    """
    Describes an instruction that can be executed by the processor.
    """

    def __init__(self):
        """
        Initialize the instruction attributes.
        """
        self.opcode = 0x00
        self.name = ""
        self.op_name = ""
        self.bytes = 0x0
        self.cycles = []

        self.operands = 0x0
        self.ops = []
        self.flags = []

    def __str__(self):
        op_name = "{}".format(self.op_name)
        if self.operands == 1:
            op_name += " {}".format(self.ops[0])
        elif self.operands == 2:
            op_name += " {} {}".format(self.ops[0], self.ops[1])
        return op_name


class OpcodeParser(object):

    def __init__(self):
        self.log = logging.getLogger("OpcodeParser")
        self.instructions = [0]*0x100
        self.cb_instructions = [0]*0x100

    @staticmethod
    def _parse_definition(op, instr):
        out = Instruction()
        out.opcode = op
        out.op_name = instr["mnemonic"]
        out.flags = instr['flags_ZHNC']
        out.operands = instr['operand_count']
        out.bytes = instr['bytes']
        out.cycles = instr['cycles']

        if out.operands > 0:
            out.ops.append(instr['operand1'])
        if out.operands > 1:
            out.ops.append(instr['operand2'])

        out.name = str(out)
        return out

    def _create_instruction(self, dataset, instr, set, type):
        opcode = int(instr, 16)
        data = dataset[type][instr]
        #self.log.debug("Loading instruction: {:02x}".format(opcode))
        set[opcode] = self._parse_definition(opcode, data)
        #self.log.debug("Loaded instruction: {}".format(set[opcode]))

    def load_instructions(self, path):
        """
        Load instruction set form a JSON dataset.
        :param path: The path to the dataset.
        :return: True if the instructions were loaded, false otherwise.
        """
        self.log.info("Loading instruction set from: {}".format(path))
        if not os.path.exists(path):
            self.log.error("Instruction set definition could not be found.")
            return False

        with open(path, "r") as handle:
            dataset = json.load(handle)
            self.log.debug("Loading un-prefixed instructions.")
            for instr in dataset['unprefixed']:
                self._create_instruction(dataset, instr,
                                         self.instructions, "unprefixed")

            self.log.debug("Loading CB-Prefixed instructions.")
            for cb in dataset['cbprefixed']:
                self._create_instruction(dataset, cb, self.cb_instructions,
                                         "cbprefixed")


