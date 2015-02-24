# Source:
# https://github.com/NewbiZ/gbemu/blob/master/scripts/retrieve_opcodes.py

# Bugs fixed and updated for Python3.

# !/usr/bin/env python

import bs4 as bs
import requests
import json

# Retrieve the webpage containing instruction set
url = 'http://www.pastraiser.com/cpu/gameboy/gameboy_opcodes.html'
html = requests.get(url).text

soup = bs.BeautifulSoup(html)

table_unprefixed, table_cbprefixed = soup.findAll('table')[:2]


def parse_table(table):
    opcodes_out = {}
    # For each row (LS 4 bits), skipping the header
    lsb = 0
    for row in table.findAll('tr')[1:]:
        msb = 0
        # For each col (MS 4 bits), skipping the header
        for col in row.findAll('td')[1:]:
            # Undefined opcodes, skip them
            if len(col) == 1 and col.text == '\xa0':
                msb += 1
                continue

            opcode_meta = {}

            values = col.contents[0].split(' ')
            opcode_meta['mnemonic'] = values[0]
            print(values[0])

            # This opcode has operands
            if len(values) > 1:
                values = values[1].split(',')
                opcode_meta['operand_count'] = len(values)
                opcode_meta['operand1'] = values[0]
                # This opcode has 2 operands
                if len(values) > 1:
                    opcode_meta['operand2'] = values[1]
            # This opcode has no operand
            else:
                opcode_meta['operand_count'] = 0

            # Retrieve bytes and cycle count
            values = col.contents[2].split('\xa0\xa0')
            print(values)
            opcode_meta['bytes'] = int(values[0])
            # Some instruction have different cycle count depending on whether actions
            # were taken or not (jumps/calls/rets)
            opcode_meta['cycles'] = [int(x) for x in values[1].split('/')]

            opcode_meta['flags_ZHNC'] = col.contents[4].split(' ')

            opcode = int(lsb << 4 | msb)
            print("[{:02x}] {}".format(opcode, opcode_meta['mnemonic']))
            opcodes_out[hex(opcode)] = opcode_meta
            msb += 1
        lsb += 1
    return opcodes_out


opcodes = {
    'unprefixed': parse_table(table_unprefixed),
    'cbprefixed': parse_table(table_cbprefixed),
}

with open("../dat/opcodes.json", "w") as handle:
    handle.write(json.dumps(opcodes, indent=2))