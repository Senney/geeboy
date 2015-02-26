import logging


class InstructionMap(object):
    
    def __init__(self, cpu, mem):
        """
        :type cpu: CPU
        :type mem: MemoryController
        :param cpu:
        :return:
        """
        self.map = []
        self._prepare_instruction_map()
        self.c = cpu
        self.m = mem

    def _prepare_instruction_map(self):
        self.map = [
            # 00
            lambda: None,                       # [00] NOP
            lambda: self.ld_rc_im16("BC"),      # [01] LD BC d16
            lambda: self.ld_mrc_r("BC", "A"),   # [02] LD (BC) A
            lambda: None,                       # [03] INC BC
            lambda: None,                       # [04] INC B
            lambda: None,                       # [05] DEC B
            lambda: self.ld_r_im8("B"),         # [06] LD B d8
            lambda: None,                       # [07] RLCA
            lambda: self.ld_mim16_sp(),         # [08] LD (a16) SP
            lambda: None,                       # [09] ADD HL BC
            lambda: self.ld_r_mrc("A", "BC"),   # [0a] LD A (BC)
            lambda: None,                       # [0b] DEC BC
            lambda: None,                       # [0c] INC C
            lambda: None,                       # [0d] DEC C
            lambda: self.ld_r_im8("C"),         # [0e] LD C d8
            lambda: None,                       # [0f] RRCA

            # 10
            lambda: None,     # [10] STOP 0
            lambda: self.ld_rc_im16("DE"),      # [11] LD DE d16
            lambda: self.ld_mrc_r("DE", "A"),   # [12] LD (DE) A
            lambda: None,     # [13] INC DE
            lambda: None,     # [14] INC D
            lambda: None,     # [15] DEC D
            lambda: self.ld_r_im8("D"),         # [16] LD D d8
            lambda: None,     # [17] RLA
            lambda: None,     # [18] JR r8
            lambda: None,     # [19] ADD HL DE
            lambda: self.ld_r_mrc("A", "DE"),   # [1a] LD A (DE)
            lambda: None,     # [1b] DEC DE
            lambda: None,     # [1c] INC E
            lambda: None,     # [1d] DEC E
            lambda: self.ld_r_im8("E"),         # [1e] LD E d8
            lambda: None,     # [1f] RRA

            # 20
            lambda: None,     # [20] JR NZ r8
            lambda: self.ld_rc_im16("HL"),      # [21] LD HL d16
            lambda: None,     # [22] LD (HL+) A TODO
            lambda: None,     # [23] INC HL
            lambda: None,     # [24] INC H
            lambda: None,     # [25] DEC H
            lambda:  self.ld_r_im8("H"),       # [26] LD H d8
            lambda: None,     # [27] DAA
            lambda: None,     # [28] JR Z r8
            lambda: None,     # [29] ADD HL HL
            lambda: None,     # [2a] LD A (HL+)
            lambda: None,     # [2b] DEC HL
            lambda: None,     # [2c] INC L
            lambda: None,     # [2d] DEC L
            lambda:  self.ld_r_im8("L"),       # [2e] LD L d8
            lambda: None,     # [2f] CPL

            # 30
            lambda: None,     # [30] JR NC r8
            lambda: self.ld_sp_im16(),         # [31] LD SP d16
            lambda: None,     # [32] LD (HL-) A TODO
            lambda: None,     # [33] INC SP
            lambda: None,     # [34] INC (HL)
            lambda: None,     # [35] DEC (HL)
            lambda: self.ld_mrc_im8("HL"),     # [36] LD (HL) d8
            lambda: None,     # [37] SCF
            lambda: None,     # [38] JR C r8
            lambda: None,     # [39] ADD HL SP
            lambda: None,     # [3a] LD A (HL-) TODO
            lambda: None,     # [3b] DEC SP
            lambda: None,     # [3c] INC A
            lambda: None,     # [3d] DEC A
            lambda: self.ld_r_im8("A"),        # [3e] LD A d8
            lambda: None,     # [3f] CCF

            # 40
            lambda: self.ld_r_r("B", "B"),     # [40] LD B B
            lambda: self.ld_r_r("B", "C"),     # [41] LD B C
            lambda: self.ld_r_r("B", "D"),     # [42] LD B D
            lambda: self.ld_r_r("B", "E"),     # [43] LD B E
            lambda: self.ld_r_r("B", "H"),     # [44] LD B H
            lambda: self.ld_r_r("B", "L"),     # [45] LD B L
            lambda: self.ld_r_mrc("B", "HL"),  # [46] LD B (HL)
            lambda: self.ld_r_r("B", "A"),     # [47] LD B A
            lambda: self.ld_r_r("C", "B"),     # [48] LD C B
            lambda: self.ld_r_r("C", "C"),     # [49] LD C C
            lambda: self.ld_r_r("C", "D"),     # [4a] LD C D
            lambda: self.ld_r_r("C", "E"),     # [4b] LD C E
            lambda: self.ld_r_r("C", "H"),     # [4c] LD C H
            lambda: self.ld_r_r("C", "L"),     # [4d] LD C L
            lambda: self.ld_r_mrc("C", "HL"),  # [4e] LD C (HL)
            lambda: self.ld_r_r("C", "A"),     # [4f] LD C A

            # 50
            lambda: self.ld_r_r("D", "B"),     # [50] LD D B
            lambda: self.ld_r_r("D", "C"),     # [51] LD D C
            lambda: self.ld_r_r("D", "D"),     # [52] LD D D
            lambda: self.ld_r_r("D", "E"),     # [53] LD D E
            lambda: self.ld_r_r("D", "H"),     # [54] LD D H
            lambda: self.ld_r_r("D", "L"),     # [55] LD D L
            lambda: self.ld_r_mrc("D", "HL"),  # [56] LD D (HL)
            lambda: self.ld_r_r("D", "A"),     # [57] LD D A
            lambda: self.ld_r_r("E", "B"),     # [58] LD E B
            lambda: self.ld_r_r("E", "C"),     # [59] LD E C
            lambda: self.ld_r_r("E", "D"),     # [5a] LD E D
            lambda: self.ld_r_r("E", "E"),     # [5b] LD E E
            lambda: self.ld_r_r("E", "H"),     # [5c] LD E H
            lambda: self.ld_r_r("E", "L"),     # [5d] LD E L
            lambda: self.ld_r_mrc("E", "HL"),  # [5e] LD E (HL)
            lambda: self.ld_r_r("E", "A"),     # [5f] LD E A

            # 60
            lambda: self.ld_r_r("H", "B"),     # [60] LD H B
            lambda: self.ld_r_r("H", "C"),     # [61] LD H C
            lambda: self.ld_r_r("H", "D"),     # [62] LD H D
            lambda: self.ld_r_r("H", "E"),     # [63] LD H E
            lambda: self.ld_r_r("H", "H"),     # [64] LD H H
            lambda: self.ld_r_r("H", "L"),     # [65] LD H L
            lambda: self.ld_r_mrc("H", "HL"),  # [66] LD H (HL)
            lambda: self.ld_r_r("H", "A"),     # [67] LD H A
            lambda: self.ld_r_r("L", "B"),     # [68] LD L B
            lambda: self.ld_r_r("L", "C"),     # [69] LD L C
            lambda: self.ld_r_r("L", "D"),     # [6a] LD L D
            lambda: self.ld_r_r("L", "E"),     # [6b] LD L E
            lambda: self.ld_r_r("L", "H"),     # [6c] LD L H
            lambda: self.ld_r_r("L", "L"),     # [6d] LD L L
            lambda: self.ld_r_mrc("L", "HL"),  # [6e] LD L (HL)
            lambda: self.ld_r_r("L", "A"),     # [6f] LD L A

            # 70
            lambda: self.ld_mrc_r("HL", "B"),  # [70] LD (HL) B
            lambda: self.ld_mrc_r("HL", "C"),  # [71] LD (HL) C
            lambda: self.ld_mrc_r("HL", "D"),  # [72] LD (HL) D
            lambda: self.ld_mrc_r("HL", "E"),  # [73] LD (HL) E
            lambda: self.ld_mrc_r("HL", "H"),  # [74] LD (HL) H
            lambda: self.ld_mrc_r("HL", "L"),  # [75] LD (HL) L
            lambda: None,     # [76] HALT
            lambda: self.ld_mrc_r("HL", "A"),  # [77] LD (HL) A
            lambda: self.ld_r_r("A", "B"),     # [78] LD A B
            lambda: self.ld_r_r("A", "C"),     # [79] LD A C
            lambda: self.ld_r_r("A", "D"),     # [7a] LD A D
            lambda: self.ld_r_r("A", "E"),     # [7b] LD A E
            lambda: self.ld_r_r("A", "H"),     # [7c] LD A H
            lambda: self.ld_r_r("A", "L"),     # [7d] LD A L
            lambda: self.ld_r_mrc("A", "HL"),  # [7e] LD A (HL)
            lambda: self.ld_r_r("A", "A"),     # [7f] LD A A

            # 80
            lambda: None,     # [80] ADD A B
            lambda: None,     # [81] ADD A C
            lambda: None,     # [82] ADD A D
            lambda: None,     # [83] ADD A E
            lambda: None,     # [84] ADD A H
            lambda: None,     # [85] ADD A L
            lambda: None,     # [86] ADD A (HL)
            lambda: None,     # [87] ADD A A
            lambda: None,     # [88] ADC A B
            lambda: None,     # [89] ADC A C
            lambda: None,     # [8a] ADC A D
            lambda: None,     # [8b] ADC A E
            lambda: None,     # [8c] ADC A H
            lambda: None,     # [8d] ADC A L
            lambda: None,     # [8e] ADC A (HL)
            lambda: None,     # [8f] ADC A A

            # 90
            lambda: None,     # [90] SUB B
            lambda: None,     # [91] SUB C
            lambda: None,     # [92] SUB D
            lambda: None,     # [93] SUB E
            lambda: None,     # [94] SUB H
            lambda: None,     # [95] SUB L
            lambda: None,     # [96] SUB (HL)
            lambda: None,     # [97] SUB A
            lambda: None,     # [98] SBC A B
            lambda: None,     # [99] SBC A C
            lambda: None,     # [9a] SBC A D
            lambda: None,     # [9b] SBC A E
            lambda: None,     # [9c] SBC A H
            lambda: None,     # [9d] SBC A L
            lambda: None,     # [9e] SBC A (HL)
            lambda: None,     # [9f] SBC A A

            # A0
            lambda: None,     # [a0] AND B
            lambda: None,     # [a1] AND C
            lambda: None,     # [a2] AND D
            lambda: None,     # [a3] AND E
            lambda: None,     # [a4] AND H
            lambda: None,     # [a5] AND L
            lambda: None,     # [a6] AND (HL)
            lambda: None,     # [a7] AND A
            lambda: None,     # [a8] XOR B
            lambda: None,     # [a9] XOR C
            lambda: None,     # [aa] XOR D
            lambda: None,     # [ab] XOR E
            lambda: None,     # [ac] XOR H
            lambda: None,     # [ad] XOR L
            lambda: None,     # [ae] XOR (HL)
            lambda: None,     # [af] XOR A

            # B0
            lambda: None,     # [b0] OR B
            lambda: None,     # [b1] OR C
            lambda: None,     # [b2] OR D
            lambda: None,     # [b3] OR E
            lambda: None,     # [b4] OR H
            lambda: None,     # [b5] OR L
            lambda: None,     # [b6] OR (HL)
            lambda: None,     # [b7] OR A
            lambda: None,     # [b8] CP B
            lambda: None,     # [b9] CP C
            lambda: None,     # [ba] CP D
            lambda: None,     # [bb] CP E
            lambda: None,     # [bc] CP H
            lambda: None,     # [bd] CP L
            lambda: None,     # [be] CP (HL)
            lambda: None,     # [bf] CP A

            # C0
            lambda: None,     # [c0] RET NZ
            lambda: None,     # [c1] POP BC
            lambda: None,     # [c2] JP NZ a16
            lambda: None,     # [c3] JP a16
            lambda: None,     # [c4] CALL NZ a16
            lambda: None,     # [c5] PUSH BC
            lambda: None,     # [c6] ADD A d8
            lambda: None,     # [c7] RST 00H
            lambda: None,     # [c8] RET Z
            lambda: None,     # [c9] RET
            lambda: None,     # [ca] JP Z a16
            lambda: None,     # [cb] PREFIX CB  >> PREFIX FUNCTION
            lambda: None,     # [cc] CALL Z a16
            lambda: None,     # [cd] CALL a16
            lambda: None,     # [ce] ADC A d8
            lambda: None,     # [cf] RST 08H

            # D0
            lambda: None,     # [d0] RET NC
            lambda: None,     # [d1] POP DE
            lambda: None,     # [d2] JP NC a16
            lambda: None,     # Not defined.
            lambda: None,     # [d4] CALL NC a16
            lambda: None,     # [d5] PUSH DE
            lambda: None,     # [d6] SUB d8
            lambda: None,     # [d7] RST 10H
            lambda: None,     # [d8] RET C
            lambda: None,     # [d9] RETI
            lambda: None,     # [da] JP C a16
            lambda: None,     # Not defined.
            lambda: None,     # [dc] CALL C a16
            lambda: None,     # Not defined.
            lambda: None,     # [de] SBC A d8
            lambda: None,     # [df] RST 18H

            # E0
            lambda: self.ld_oim8_r("A"),      # [e0] LDH (a8) A
            lambda: None,     # [e1] POP HL
            lambda: self.ld_omr_r("C", "A"),  # [e2] LD (C) A
            lambda: None,     # Not defined.
            lambda: None,     # Not defined.
            lambda: None,     # [e5] PUSH HL
            lambda: None,     # [e6] AND d8
            lambda: None,     # [e7] RST 20H
            lambda: None,     # [e8] ADD SP r8
            lambda: None,     # [e9] JP (HL)
            lambda: self.ld_mim16_r("A"),     # [ea] LD (a16) A
            lambda: None,     # Not defined.
            lambda: None,     # Not defined.
            lambda: None,     # Not defined.
            lambda: None,     # [ee] XOR d8
            lambda: None,     # [ef] RST 28H

            # F0
            lambda: self.ld_r_oim8("A"),      # [f0] LDH A (a8)
            lambda: None,     # [f1] POP AF
            lambda: self.ld_r_omr("A", "C"),  # [f2] LD A (C)
            lambda: None,     # [f3] DI
            lambda: None,     # Not defined.
            lambda: None,     # [f5] PUSH AF
            lambda: None,     # [f6] OR d8
            lambda: None,     # [f7] RST 30H
            lambda: self.ldhl_sp_im8(),       # [f8] LD HL SP+r8
            lambda: self.ld_sp_rc("HL"),      # [f9] LD SP HL
            lambda: self.ld_r_mim16("A"),     # [fa] LD A (a16)
            lambda: None,     # [fb] EI
            lambda: None,     # Not defined.
            lambda: None,     # Not defined.
            lambda: None,     # [fe] CP d8
            lambda: None,     # [ff] RST 38H
        ]

    def combo_s(self, rc):
        return self.combo(rc[0], rc[1])

    def combo(self, r1, r2):
        return self.c.r[r1] << 8 | self.c.r[r2]

    def ld_r_im8(self, reg):
        self.c.r[reg] = (self.m.read(self.c.pc + 1)) & 0xFF

    def ld_r_r(self, r1, r2):
        self.c.r[r1] = self.c.r[r2]

    def ld_r_mrc(self, r1, rc):
        """Load a register with a memory reference in a register combo (e.g. (HL))"""
        self.c.r[r1] = self.m.read(self.combo_s(rc))

    def ld_mrc_r(self, r1, rc):
        self.m.write(self.combo_s(rc), self.c.r[r1])

    def ld_r_mim16(self, r1):
        mem = (self.m.read(self.c.pc + 1) << 8) | self.m.read(self.c.pc + 2)
        self.c.r[r1] = self.m.read(mem)

    def ld_r_im16(self, r1):
        """Load a register with an immediate value"""
        self.c.r[r1] = self.m.read(self.c.pc + 1)

    def ld_mim16_r(self, r1):
        """Load an immediate memory address with a register value."""
        mem = (self.m.read(self.c.pc + 1) << 8) | self.m.read(self.c.pc + 2)
        self.m.write(mem, self.c.r[r1])

    def ld_r_omr(self, r1, r2):
        """Load a register with a value at 0xFF00 + r2."""
        self.c.r[r1] = self.m.read(self.c.r[r2])

    def ld_omr_r(self, r1, r2):
        self.m.write(0xFF00 + self.c.r[r1], self.c.r[r2])

    def ld_r_oim8(self, r1):
        self.c.r[r1] = self.m.read(0xFF00 + self.m.read(self.c.pc + 1))

    def ld_oim8_r(self, r1):
        self.m.write(0xFF00 + self.m.read(self.c.pc + 1), self.c.r[r1])

    def ld_rc_im16(self, rc):
        self.c.r[rc[1]] = self.m.read(self.c.pc + 1)
        self.c.r[rc[0]] = self.m.read(self.c.pc + 2)

    def ld_sp_rc(self, rc):
        self.c.sp = self.combo_s(rc)

    def ldhl_sp_im8(self):
        """The immediate value is signed."""
        n = self.m.read(self.c.pc + 1)
        if n > 127:
            n = -((~n + 1) & 255)
        n += self.c.sp
        self.c.r["H"] = (n >> 8) & 0xFF
        self.c.r["L"] = n & 0xFF
        # TODO: Implement the flags for this operation.

    def ld_sp_im16(self):
        mem = (self.m.read(self.c.pc + 1) << 8) | self.m.read(self.c.pc + 2)
        self.c.sp = mem

    def ld_mim16_sp(self):
        mem = (self.m.read(self.c.pc + 1) << 8) | self.m.read(self.c.pc + 2)
        self.m.write(mem, (self.c.sp >> 8) & 0xFF)
        self.m.write(mem+1, self.c.sp & 0xFF)

    def ld_mrc_im8(self, rc):
        mem = self.m.read(self.c.pc + 1)
        self.c.r[rc[0]] = 0
        self.c.r[rc[1]] = mem


class CPU(object):

    def __init__(self, cart, mem, ops):
        """
        :type cart: Cartridge
        :type mem: MemoryController
        :type ops: OpcodeParser
        :param cart: The loaded Cartridge
        :param mem: The memory unit, which we will use for access.
        :param ops: The OpcodeParser which will provide timing and instruction information
        :return:
        """
        self.cart = cart
        self.mem = mem
        self.ops = ops
        self._log = logging.getLogger("CPU")
        self.halt = False
        self.r = {
            "A": 0,
            "F": 0,
            "B": 0,
            "C": 0,
            "D": 0,
            "E": 0,
            "H": 0,
            "L": 0,
        }

        self.sp = 0xFFFE    # Per GBCPUMan page 64
        self.pc = 0x100      # We start at 100.
        self.f = {
            "Z": 0,   # Zero bit
            "N": 0,   # Subtract
            "H": 0,   # Half-carry
            "C": 0,   # Carry
        }

        self.instructions = InstructionMap(self, self.mem)

    def run(self):

        while True:
            # Get the next instruction from the ROM
            # Run the instruction
            if self.halt and self.mem.interrupts_enabled:
                # TODO: Handle interrupts, and handle
                # the HALT issue on Gameboy as specified
                # on page 20 of the Gameboy CPU manual.
                continue

            data = self.mem.read(self.pc)
            func = self.instructions.map[data]
            instr = self.ops.instructions[data]
            self._log.debug("Instruction: 0x{:02x}: [0x{:02x}] -> {}".format(self.pc, data, instr))