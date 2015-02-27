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
            lambda: self.inc_r("B"),            # [04] INC B
            lambda: None,                       # [05] DEC B
            lambda: self.ld_r_im8("B"),         # [06] LD B d8
            lambda: None,                       # [07] RLCA
            lambda: self.ld_mim16_sp(),         # [08] LD (a16) SP
            lambda: None,                       # [09] ADD HL BC
            lambda: self.ld_r_mrc("A", "BC"),   # [0a] LD A (BC)
            lambda: None,                       # [0b] DEC BC
            lambda: self.inc_r("C"),            # [0c] INC C
            lambda: None,                       # [0d] DEC C
            lambda: self.ld_r_im8("C"),         # [0e] LD C d8
            lambda: None,                       # [0f] RRCA

            # 10
            lambda: None,     # [10] STOP 0
            lambda: self.ld_rc_im16("DE"),      # [11] LD DE d16
            lambda: self.ld_mrc_r("DE", "A"),   # [12] LD (DE) A
            lambda: None,     # [13] INC DE
            lambda: self.inc_r("D"),              # [14] INC D
            lambda: None,     # [15] DEC D
            lambda: self.ld_r_im8("D"),         # [16] LD D d8
            lambda: None,     # [17] RLA
            lambda: self.jp_oim8(),             # [18] JR r8
            lambda: None,     # [19] ADD HL DE
            lambda: self.ld_r_mrc("A", "DE"),   # [1a] LD A (DE)
            lambda: None,     # [1b] DEC DE
            lambda: self.inc_r("E"),            # [1c] INC E
            lambda: None,     # [1d] DEC E
            lambda: self.ld_r_im8("E"),         # [1e] LD E d8
            lambda: None,     # [1f] RRA

            # 20
            lambda: self.jp_cc_oim8("Z", 0),    # [20] JR NZ r8
            lambda: self.ld_rc_im16("HL"),      # [21] LD HL d16
            lambda: self.ld_hli_r("A"),         # [22] LD (HL+) A
            lambda: None,     # [23] INC HL
            lambda: self.inc_r("H"),           # [24] INC H
            lambda: None,     # [25] DEC H
            lambda: self.ld_r_im8("H"),        # [26] LD H d8
            lambda: None,     # [27] DAA
            lambda: self.jp_cc_oim8("Z", 1),   # [28] JR Z r8
            lambda: None,     # [29] ADD HL HL
            lambda: self.ld_r_hli("A"),        # [2a] LD A (HL+)
            lambda: None,     # [2b] DEC HL
            lambda: self.inc_r("L"),           # [2c] INC L
            lambda: None,     # [2d] DEC L
            lambda: self.ld_r_im8("L"),        # [2e] LD L d8
            lambda: None,     # [2f] CPL

            # 30
            lambda: self.jp_cc_oim8("C", 0),   # [30] JR NC r8
            lambda: self.ld_sp_im16(),         # [31] LD SP d16
            lambda: self.ld_hld_r("A"),        # [32] LD (HL-) A
            lambda: None,     # [33] INC SP
            lambda: self.inc_mrc("HL"),        # [34] INC (HL)
            lambda: None,     # [35] DEC (HL)
            lambda: self.ld_mrc_im8("HL"),     # [36] LD (HL) d8
            lambda: None,     # [37] SCF
            lambda: self.jp_cc_oim8("C", 1),   # [38] JR C r8
            lambda: None,     # [39] ADD HL SP
            lambda: self.ld_r_hld("A"),        # [3a] LD A (HL-)
            lambda: None,     # [3b] DEC SP
            lambda: self.inc_r("A"),           # [3c] INC A
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
            lambda: self.add_r_r("A", "B"),    # [80] ADD A B
            lambda: self.add_r_r("A", "C"),    # [81] ADD A C
            lambda: self.add_r_r("A", "D"),    # [82] ADD A D
            lambda: self.add_r_r("A", "E"),    # [83] ADD A E
            lambda: self.add_r_r("A", "H"),    # [84] ADD A H
            lambda: self.add_r_r("A", "L"),    # [85] ADD A L
            lambda: self.add_r_mrc("A", "HL"),  # [86] ADD A (HL)
            lambda: self.add_r_r("A", "A"),    # [87] ADD A A
            lambda: self.adc_r_r("A", "B"),    # [88] ADC A B
            lambda: self.adc_r_r("A", "C"),    # [89] ADC A C
            lambda: self.adc_r_r("A", "D"),    # [8a] ADC A D
            lambda: self.adc_r_r("A", "E"),    # [8b] ADC A E
            lambda: self.adc_r_r("A", "H"),    # [8c] ADC A H
            lambda: self.adc_r_r("A", "L"),    # [8d] ADC A L
            lambda: self.adc_r_mrc("A", "HL"),    # [8e] ADC A (HL)
            lambda: self.adc_r_r("A", "A"),    # [8f] ADC A A

            # 90
            lambda: self.sub_r_r("A", "B"),    # [90] SUB B
            lambda: self.sub_r_r("A", "C"),    # [91] SUB C
            lambda: self.sub_r_r("A", "D"),    # [92] SUB D
            lambda: self.sub_r_r("A", "E"),    # [93] SUB E
            lambda: self.sub_r_r("A", "H"),    # [94] SUB H
            lambda: self.sub_r_r("A", "L"),    # [95] SUB L
            lambda: self.sub_r_mrc("A", "HL"),    # [96] SUB (HL)
            lambda: self.sub_r_r("A", "A"),    # [97] SUB A
            lambda: self.sbc_r_r("A", "B"),    # [98] SBC A B
            lambda: self.sbc_r_r("A", "C"),    # [99] SBC A C
            lambda: self.sbc_r_r("A", "D"),    # [9a] SBC A D
            lambda: self.sbc_r_r("A", "E"),    # [9b] SBC A E
            lambda: self.sbc_r_r("A", "H"),    # [9c] SBC A H
            lambda: self.sbc_r_r("A", "L"),    # [9d] SBC A L
            lambda: self.sbc_r_mrc("A", "HL"),    # [9e] SBC A (HL)
            lambda: self.sbc_r_r("A", "A"),    # [9f] SBC A A

            # A0
            lambda: self.and_r_r("A", "B"),    # [a0] AND B
            lambda: self.and_r_r("A", "C"),    # [a1] AND C
            lambda: self.and_r_r("A", "D"),    # [a2] AND D
            lambda: self.and_r_r("A", "E"),    # [a3] AND E
            lambda: self.and_r_r("A", "H"),    # [a4] AND H
            lambda: self.and_r_r("A", "L"),    # [a5] AND L
            lambda: self.and_r_mrc("A", "HL"),  # [a6] AND (HL)
            lambda: self.and_r_r("A", "A"),    # [a7] AND A
            lambda: self.xor_r_r("A", "B"),    # [a8] XOR B
            lambda: self.xor_r_r("A", "C"),    # [a9] XOR C
            lambda: self.xor_r_r("A", "D"),    # [aa] XOR D
            lambda: self.xor_r_r("A", "E"),    # [ab] XOR E
            lambda: self.xor_r_r("A", "H"),    # [ac] XOR H
            lambda: self.xor_r_r("A", "L"),    # [ad] XOR L
            lambda: self.xor_r_mrc("A", "HL"),  # [ae] XOR (HL)
            lambda: self.xor_r_r("A", "A"),    # [af] XOR A

            # B0
            lambda: self.or_r_r("A", "B"),     # [b0] OR B
            lambda: self.or_r_r("A", "C"),     # [b1] OR C
            lambda: self.or_r_r("A", "D"),     # [b2] OR D
            lambda: self.or_r_r("A", "E"),     # [b3] OR E
            lambda: self.or_r_r("A", "H"),     # [b4] OR H
            lambda: self.or_r_r("A", "L"),     # [b5] OR L
            lambda: self.or_r_mrc("A", "HL"),  # [b6] OR (HL)
            lambda: self.or_r_r("A", "A"),     # [b7] OR A
            lambda: self.cp_r_r("A", "B"),     # [b8] CP B
            lambda: self.cp_r_r("A", "C"),     # [b9] CP C
            lambda: self.cp_r_r("A", "D"),     # [ba] CP D
            lambda: self.cp_r_r("A", "E"),     # [bb] CP E
            lambda: self.cp_r_r("A", "H"),     # [bc] CP H
            lambda: self.cp_r_r("A", "L"),     # [bd] CP L
            lambda: self.cp_r_mrc("A", "HL"),  # [be] CP (HL)
            lambda: self.cp_r_r("A", "A"),     # [bf] CP A

            # C0
            lambda: self.ret_cc("Z", 0),        # [c0] RET NZ
            lambda: self.pop("BC"),             # [c1] POP BC
            lambda: self.jp_cc_im16("Z", 0),    # [c2] JP NZ a16
            lambda: self.jp_im16(),             # [c3] JP a16
            lambda: self.call_cc("Z", 0),       # [c4] CALL NZ a16
            lambda: self.push("BC"),            # [c5] PUSH BC
            lambda: self.add_r_im8("A"),        # [c6] ADD A d8
            lambda: self.rst_im8(0x0),          # [c7] RST 00H
            lambda: self.ret_cc("Z", 1),        # [c8] RET Z
            lambda: self.ret(),                 # [c9] RET
            lambda: self.jp_cc_im16("Z", 1),    # [ca] JP Z a16
            lambda: None,     # [cb] PREFIX CB  >> PREFIX FUNCTION
            lambda: self.call_cc("Z", 1),       # [cc] CALL Z a16
            lambda: self.call(),                # [cd] CALL a16
            lambda: self.adc_r_im8("A"),        # [ce] ADC A d8
            lambda: self.rst_im8(0x08),         # [cf] RST 08H

            # D0
            lambda: self.ret_cc("C", 0),        # [d0] RET NC
            lambda: self.pop("DE"),             # [d1] POP DE
            lambda: self.jp_cc_im16("C", 0),    # [d2] JP NC a16
            lambda: None,                       # Not defined.
            lambda: self.call_cc("C", 0),       # [d4] CALL NC a16
            lambda: self.push("DE"),            # [d5] PUSH DE
            lambda: self.sub_r_im8("A"),        # [d6] SUB d8
            lambda: self.rst_im8(0x10),         # [d7] RST 10H
            lambda: self.ret_cc("C", 1),        # [d8] RET C
            lambda: self.reti(),                # [d9] RETI
            lambda: self.jp_cc_im16("C", 1),    # [da] JP C a16
            lambda: None,                       # Not defined.
            lambda: self.call_cc("C", 1),       # [dc] CALL C a16
            lambda: None,                       # Not defined.
            lambda: self.sbc_r_im8("A"),        # [de] SBC A d8
            lambda: self.rst_im8(0x18),         # [df] RST 18H

            # E0
            lambda: self.ld_oim8_r("A"),        # [e0] LDH (a8) A
            lambda: self.pop("HL"),             # [e1] POP HL
            lambda: self.ld_omr_r("C", "A"),    # [e2] LD (C) A
            lambda: None,                       # Not defined.
            lambda: None,                       # Not defined.
            lambda: self.push("HL"),            # [e5] PUSH HL
            lambda: self.and_r_im8("A"),        # [e6] AND d8
            lambda: self.rst_im8(0x20),         # [e7] RST 20H
            lambda: None,     # [e8] ADD SP r8
            lambda: self.jp_mrc("HL"),          # [e9] JP (HL)
            lambda: self.ld_mim16_r("A"),       # [ea] LD (a16) A
            lambda: None,                       # Not defined.
            lambda: None,                       # Not defined.
            lambda: None,                       # Not defined.
            lambda: self.xor_r_im8("A"),        # [ee] XOR d8
            lambda: self.rst_im8(0x28),         # [ef] RST 28H

            # F0
            lambda: self.ld_r_oim8("A"),        # [f0] LDH A (a8)
            lambda: self.pop("AF"),             # [f1] POP AF
            lambda: self.ld_r_omr("A", "C"),    # [f2] LD A (C)
            lambda: None,     # [f3] DI
            lambda: None,                       # Not defined.
            lambda: self.push("AF"),            # [f5] PUSH AF
            lambda: self.or_r_im8("A"),         # [f6] OR d8
            lambda: self.rst_im8(0x30),         # [f7] RST 30H
            lambda: self.ldhl_sp_im8(),         # [f8] LD HL SP+r8
            lambda: self.ld_sp_rc("HL"),        # [f9] LD SP HL
            lambda: self.ld_r_mim16("A"),       # [fa] LD A (a16)
            lambda: None,     # [fb] EI
            lambda: None,                       # Not defined.
            lambda: None,                       # Not defined.
            lambda: self.cp_r_im8("A"),         # [fe] CP d8
            lambda: self.rst_im8(0x38),         # [ff] RST 38H
        ]

    def combo_s(self, rc):
        return self.combo(rc[0], rc[1])

    def combo(self, r1, r2):
        return self.c.r[r1] << 8 | self.c.r[r2]

    def get_im16(self):
        mem = (self.m.read(self.c.pc + 1)) | (self.m.read(self.c.pc + 2) << 8)
        #mem = (self.m.read(self.c.pc + 1) << 8) | self.m.read(self.c.pc + 2)
        return mem

    def ld_r_im8(self, reg):
        self.c.r[reg] = (self.m.read(self.c.pc + 1)) & 0xFF

    def ld_r_r(self, r1, r2):
        self.c.r[r1] = self.c.r[r2]

    def ld_r_mrc(self, r1, rc):
        """Load a register with a memory reference in a register combo (e.g. (HL))"""
        self.c.r[r1] = self.m.read(self.combo_s(rc))

    def ld_mrc_r(self, rc, r1):
        self.m.write(self.combo_s(rc), self.c.r[r1])

    def ld_r_mim16(self, r1):
        mem = self.get_im16()
        self.c.r[r1] = self.m.read(mem)

    def ld_r_im16(self, r1):
        """Load a register with an immediate value"""
        self.c.r[r1] = self.m.read(self.c.pc + 1)

    def ld_mim16_r(self, r1):
        """Load an immediate memory address with a register value."""
        mem = self.get_im16()
        self.m.write(mem, self.c.r[r1])

    def ld_r_omr(self, r1, r2):
        """Load a register with a value at 0xFF00 + r2."""
        self.c.r[r1] = self.m.read(0xFF00 + self.c.r[r2])

    def ld_omr_r(self, r1, r2):
        self.m.write(0xFF00 + self.c.r[r1], self.c.r[r2])

    def ld_r_oim8(self, r1):
        self.c.r[r1] = self.m.read(0xFF00 + self.m.read(self.c.pc + 1))

    def ld_oim8_r(self, r1):
        self.m.write(0xFF00 + self.m.read(self.c.pc + 1), self.c.r[r1])

    def ld_rc_im16(self, rc):
        self.c.r[rc[1]] = self.m.read(self.c.pc + 1)
        self.c.r[rc[0]] = self.m.read(self.c.pc + 2)

    def ld_hli_r(self, r1):
        hl = self.combo_s("HL")
        self.m.write(hl, r1)

        hl += 1
        self.c.r["H"] = (hl >> 8) & 0xFF
        self.c.r["L"] = hl & 0xFF

    def ld_r_hli(self, r1):
        hl = self.combo_s("HL")
        self.c.r[r1] = self.m.read(hl)

        hl += 1
        self.c.r["H"] = (hl >> 8) & 0xFF
        self.c.r["L"] = hl & 0xFF

    def ld_hld_r(self, r1):
        hl = self.combo_s("HL")
        self.m.write(hl, r1)

        hl -= 1
        self.c.r["H"] = (hl >> 8) & 0xFF
        self.c.r["L"] = hl & 0xFF

    def ld_r_hld(self, r1):
        hl = self.combo_s("HL")
        self.c.r[r1] = self.m.read(hl)

        hl -= 1
        self.c.r["H"] = (hl >> 8) & 0xFF
        self.c.r["L"] = hl & 0xFF

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
        mem = self.get_im16()
        self.c.sp = mem

    def ld_mim16_sp(self):
        mem = self.get_im16()
        self.m.write(mem, (self.c.sp >> 8) & 0xFF)
        self.m.write(mem+1, self.c.sp & 0xFF)

    def ld_mrc_im8(self, rc):
        mem = self.m.read(self.c.pc + 1)
        self.c.r[rc[0]] = 0
        self.c.r[rc[1]] = mem

    def push(self, rc):
        """Pushes the value from a register pair on to the stack."""
        self.m.write(self.c.sp - 1, self.c.r[rc[0]])
        self.m.write(self.c.sp - 2, self.c.r[rc[1]])
        self.c.sp -= 2

    def pop(self, rc):
        """Pops two bytes off of the stack."""
        self.c.r[rc[1]] = self.m.read(self.c.sp)
        self.c.r[rc[0]] = self.m.read(self.c.sp+1)
        self.c.sp += 2

    """
    Note that for each of the *JUMP* instructions, we subtract the byte size of the instruction
    to negate the Program Counter increment.
    """

    def jp_im16(self):
        self.c.pc = self.get_im16() - 3

    def jp_cc_im16(self, flag, val):
        f = self.c.f[flag]
        if f == val:
            self.c.pc = self.get_im16() - 3

    def jp_mrc(self, rc):
        self.c.pc = self.m.read(self.combo_s(rc)) - 1

    def jp_oim8(self):
        new_pc = self.c.pc + self.m.read(self.c.pc + 1) - 2
        self.c.pc = new_pc

    def jp_cc_oim8(self, flag, val):
        f = self.c.f[flag]
        if f == val:
            self.c.pc = self.c.pc + self.m.read(self.c.pc + 1) - 2

    def call(self):
        self.m.write(self.c.sp - 1, (self.c.pc >> 8) & 0xFF)
        self.m.write(self.c.sp - 2, self.c.pc & 0xFF)
        self.c.sp -= 2

        self.c.pc = self.get_im16() - 3

    def call_cc(self, flag, val):
        f = self.c.f[flag]
        if f == val:
            self.call()

    def rst_im8(self, off):
        self.m.write(self.c.sp - 1, (self.c.pc >> 8) & 0xFF)
        self.m.write(self.c.sp - 2, self.c.pc & 0xFF)
        self.c.sp -= 2

        self.c.pc = off + self.m.read(self.c.pc + 1) - 2

    def ret(self):
        self.c.pc = (self.m.read(self.c.sp + 1) << 8) | self.m.read(self.c.sp) - 1
        self.c.sp += 2

    def ret_cc(self, flag, val):
        f = self.c.f[flag]
        if f == val:
            self.ret()

    def reti(self):
        self.ret()
        self.m.interrupts_enabled = True

    """ALU Functions"""

    """Addition"""
    def _add_flags(self, op1, op2, res):
        self.c.f["C"] = 1 if res > 255 else 0
        self.c.f["H"] = 1 if ((op1 & 0xF) + (op2 & 0xF) & 0x10) > 0 else 0
        self.c.f["Z"] = 1 if res == 0 else 0
        self.c.f["N"] = 0

    def _add_8b(self, op1, op2):
        res = op1 + op2
        self._add_flags(op1, op2, res)
        return res & 0xFF

    def add_r_im8(self, r1):
        op1 = self.c.r[r1]
        op2 = self.m.read(self.c.pc + 1)
        ret = self._add_8b(op1, op2) & 0xFF
        self.c.r[r1] = ret

    def add_r_r(self, r1, r2):
        op1 = self.c.r[r1]
        op2 = self.c.r[r2]
        ret = self._add_8b(op1, op2) & 0xFF
        self.c.r[r1] = ret

    def add_r_mrc(self, r1, rc):
        op1 = self.c.r[r1]
        op2 = self.m.read(self.combo_s(rc))
        ret = self._add_8b(op1, op2) & 0xFF
        self.c.r[r1] = ret

    def adc_r_im8(self, r1):
        op1 = self.c.r[r1]
        op2 = self.m.read(self.c.pc + 1) + self.c.f["C"]
        ret = self._add_8b(op1, op2) & 0xFF
        self.c.r[r1] = ret

    def adc_r_r(self, r1, r2):
        op1 = self.c.r[r1]
        op2 = self.c.r[r2] + self.c.f["C"]
        ret = self._add_8b(op1, op2) & 0xFF
        self.c.r[r1] = ret

    def adc_r_mrc(self, r1, rc):
        op1 = self.c.r[r1]
        op2 = self.m.read(self.combo_s(rc)) + self.c.f["C"]
        ret = self._add_8b(op1, op2) & 0xFF
        self.c.r[r1] = ret

    def _inc_flags(self, op1):
        self.c.f['Z'] = 1 if op1 == 0 else 0
        self.c.f['N'] = 0
        self.c.f['H'] = 1 if ((op1 & 0xF) + 1 & 0x10) > 0 else 0

    def inc_r(self, r1):
        op1 = self.c.r[r1]
        op1 += 1
        self._inc_flags(op1)
        self.c.r[r1] = op1

    def inc_mrc(self, rc):
        op1 = self.m.read(self.combo_s(rc))
        op1 += 1
        self._inc_flags(op1)
        self.m.write(self.combo_s(rc), op1)

    """Subtraction"""
    def _sub_8b(self, op1, op2):
        ret = op1 - op2
        self._sub_flags(op1, op2, ret)
        return ret

    def _sub_flags(self, op1, op2, ret):
        self.c.f["C"] = 1 if ret < 0 else 0
        self.c.f["H"] = 1 if (((op1 & 0xF) - (op2 & 0xF)) & 0x10) > 0 else 0
        self.c.f["N"] = 1
        self.c.f["Z"] = 1 if ret == 0 else 0

    def sub_r_r(self, r1, r2):
        op1 = self.c.r[r1]
        op2 = self.c.r[r2]
        ret = self._sub_8b(op1, op2)
        self.c.r[r1] = ret & 0xFF

    def sub_r_mrc(self, r1, rc):
        op1 = self.c.r[r1]
        op2 = self.m.read(self.combo_s(rc))
        ret = self._sub_8b(op1, op2)
        self.c.r[r1] = ret & 0xFF

    def sub_r_im8(self, r1):
        op1 = self.c.r[r1]
        op2 = self.m.read(self.c.pc + 1)
        ret = self._sub_8b(op1, op2)
        self.c.r[r1] = ret & 0xFF

    def sbc_r_r(self, r1, r2):
        op1 = self.c.r[r1]
        op2 = self.c.r[r2] + self.c.f["C"]
        ret = self._sub_8b(op1, op2)
        self.c.r[r1] = ret & 0xFF

    def sbc_r_mrc(self, r1, rc):
        op1 = self.c.r[r1]
        op2 = self.m.read(self.combo_s(rc)) + self.c.f["C"]
        ret = self._sub_8b(op1, op2)
        self.c.r[r1] = ret & 0xFF

    def sbc_r_im8(self, r1):
        op1 = self.c.r[r1]
        op2 = self.m.read(self.c.pc + 1) + self.c.f["C"]
        ret = self._sub_8b(op1, op2)
        self.c.r[r1] = ret & 0xFF

    def _cp_flags(self, op1, op2, ret):
        self.c.f['Z'] = 1 if ret == 0 else 0
        self.c.f['N'] = 1
        self.c.f['H'] = 1 if (((op1 & 0xF) - (op2 & 0xF)) & 0x10) == 0 else 0
        self.c.f['C'] = 1 if op1 < op2 else 0

    def cp_r_r(self, r1, r2):
        op1 = self.c.r[r1]
        op2 = self.c.r[r2]
        ret = op1 - op2
        self._cp_flags(op1, op2, ret)

    def cp_r_mrc(self, r1, rc):
        op1 = self.c.r[r1]
        op2 = self.m.read(self.combo_s(rc))
        self._cp_flags(op1, op2, op1-op2)

    def cp_r_im8(self, r1):
        op1 = self.c.r[r1]
        op2 = self.m.read(self.c.pc + 1)
        self._cp_flags(op1, op2, op1-op2)

    """Bitwise Operations"""

    def _and_flags(self, ret):
        self.c.f["Z"] = 1 if ret == 0 else 0
        self.c.f["N"] = 0
        self.c.f["H"] = 1
        self.c.f["C"] = 0

    def and_r_r(self, r1, r2):
        op1 = self.c.r[r1]
        op2 = self.c.r[r2]
        ret = (op1 & op2) & 0xFF
        self._and_flags(ret)
        self.c.r[r1] = ret

    def and_r_mrc(self, r1, rc):
        op1 = self.c.r[r1]
        op2 = self.m.read(self.combo_s(rc))
        ret = (op1 & op2) & 0xFF
        self._and_flags(ret)
        self.c.r[r1] = ret

    def and_r_im8(self, r1):
        op1 = self.c.r[r1]
        op2 = self.m.read(self.c.pc + 1)
        ret = (op1 & op2) & 0xFF
        self._and_flags(ret)
        self.c.r[r1] = ret

    def _or_flags(self, ret):
        self.c.f["Z"] = 1 if ret == 0 else 0
        self.c.f["N"] = 0
        self.c.f["H"] = 0
        self.c.f["C"] = 0

    def or_r_r(self, r1, r2):
        op1 = self.c.r[r1]
        op2 = self.c.r[r2]
        ret = (op1 | op2) & 0xFF
        self._or_flags(ret)
        self.c.r[r1] = ret

    def or_r_mrc(self, r1, rc):
        op1 = self.c.r[r1]
        op2 = self.m.read(self.combo_s(rc))
        ret = (op1 | op2) & 0xFF
        self._or_flags(ret)
        self.c.r[r1] = ret

    def or_r_im8(self, r1):
        op1 = self.c.r[r1]
        op2 = self.m.read(self.c.pc + 1)
        ret = (op1 | op2) & 0xFF
        self._or_flags(ret)
        self.c.r[r1] = ret

    def xor_r_r(self, r1, r2):
        op1 = self.c.r[r1]
        op2 = self.c.r[r2]
        ret = (op1 ^ op2) & 0xFF
        self._or_flags(ret)
        self.c.r[r1] = ret

    def xor_r_mrc(self, r1, rc):
        op1 = self.c.r[r1]
        op2 = self.m.read(self.combo_s(rc))
        ret = (op1 ^ op2) & 0xFF
        self._or_flags(ret)
        self.c.r[r1] = ret

    def xor_r_im8(self, r1):
        op1 = self.c.r[r1]
        op2 = self.m.read(self.c.pc + 1)
        ret = (op1 ^ op2) & 0xFF
        self._or_flags(ret)
        self.c.r[r1] = ret


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
            if data == 0xCB:
                self._log.debug("[{:02x}] CB not implemented yet.".format(self.pc))
                skip_instr = self.ops.cb_instructions[self.mem.read(self.pc+1)]
                self.pc += skip_instr.bytes
                self._log.debug("Skipped instruction: {}".format(skip_instr))
                continue

            func = self.instructions.map[data]
            instr = self.ops.instructions[data]

            #self._log.debug("Instruction: 0x{:02x}: [0x{:02x}] -> {}".format(self.pc, data, instr))
            try:
                if func:
                    func()
                    #self.stack_dump()
            except Exception as e:
                self.stack_dump()
                self._log.exception(e)
                self._log.fatal("Unable to continue")

            self.pc += instr.bytes
            #input()

    def stack_dump(self):
        message = ""
        message += "STACK TRACE " + ("=" * 66) + "\n"
        message += "Registers: \n"
        for r in self.r:
            if self.r[r] is not None:
                message += "   {}: 0x{:02x}\n".format(r, self.r[r])
            else:
                message += "   {}: {}\n".format(r, "ERR")
        message += "   {}: 0x{:02x}\n".format("sp", self.sp)
        message += "   {}: 0x{:02x}\n".format("pc", self.pc)
        self._log.error(message)

