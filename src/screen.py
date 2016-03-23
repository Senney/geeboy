"""
Required Hardware Registers:
    FF40 -> LCDC -> LCD Control
    FF41 -> STAT -> LCD Status
    FF42 -> SCY  -> Scroll Y (Background)
    FF43 -> SCX  -> Scroll X (Background)
    FF44 -> LY   -> LCD Y-Coordinate
    FF45 -> LYC  -> The LYC compares itself with the LY. If the
                    values are the same it causes the STAT to
                    set the coincident flag.
    FF46 -> DMA  -> DMA Transfer start address
    FF47 -> BGP  -> Background palette
    FF48 -> OBP0 -> Colors for sprite palette 0. 0 = Transparent.
    FF49 -> OBP1 -> Colors for sprite palette 1.
    FF4A -> WY   -> Window Y
    FF4B -> WX   -> Window X
"""
import logging


class Screen(object):

    def __init__(self):
        """
        :type cpu: CPU
        :type mem: MemoryController
        :param cpu:
        :return:
        """
        self._log = logging.getLogger("Screen")
        self._cpu = None

        self.cycles = 0

        self._lcd_control = 1
        self._window_tile_map = 0
        self._window_display = 0
        self._bg_tile_data = 1
        self._bg_tile_map = 0
        self._obj_sprite_size = 0
        self._obj_display = 0
        self._bg_display = 1

        self._cur_line = 0

    def _get_lcdc(self):
        return (self._lcd_control << 7) | (self._window_tile_map << 6) | (self._window_display << 5) | \
               (self._bg_tile_data << 4) | (self._bg_tile_map << 3) | (self._obj_sprite_size << 2) | \
               (self._obj_display << 1) | self._bg_display

    def _set_lcdc(self, value):
        self._lcd_control = value & 0b10000000
        self._window_tile_map = value & 0b01000000
        self._window_display = value & 0b00100000
        self._bg_tile_data = value & 0b00010000
        self._bg_tile_map = value & 0b00001000
        self._obj_sprite_size = value & 0b00000100
        self._obj_display = value & 0b00000010
        self._bg_display = value & 0b00000000

    def in_range(self, byte):
        # TODO: Implement remaining screen registers.
        return byte == 0xFF40

    def read(self, byte):
        op = byte - 0xFF40
        if op == 0:
            return self._get_lcdc()

    def write(self, byte, value):
        op = byte - 0xFF40
        if op == 0:
            self._set_lcdc(value)

    def vblank(self):
        self._log.debug("vblank called.")
        self._cpu.vblank()

    def tick(self, cycles):

        self.cycles += cycles
        if self.cycles >= 83836:
            self.vblank()
            self.cycles -= 83836

    def set_cpu(self, cpu):
        self._cpu = cpu


