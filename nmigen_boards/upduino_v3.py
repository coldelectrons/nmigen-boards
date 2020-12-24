import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .resources import *


__all__ = ["UpduinoV3Platform"]


class UpduinoV3Platform(LatticeICE40Platform):
    # Supposed to be backwards compatible to
    # the V2 board
    device      = "iCE40UP5K"
    package     = "SG48"
    default_clk = "SB_HFOSC"
    hfosc_div   = 0
    resources   = [
        *LEDResources(pins="39 40 41", invert=True,
                      attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("led_g", 0, PinsN("39", dir="o"),
                 Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("led_b", 0, PinsN("40", dir="o"),
                 Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("led_r", 0, PinsN("41", dir="o"),
                 Attrs(IO_STANDARD="SB_LVCMOS")),

        *SPIFlashResources(0,
            cs_n="16", clk="15", cipo="17", copi="14",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),
        # Solder jumper on SJ16 (labeled OSC) to enable.
        Resource("clk12", 0, Pins("12", dir="i"),
                 Clock(12e6), Attrs(IO_STANDARD="SB_LVCMOS")),
    ]
    connectors  = [
        # "Left" row of header pins (JP3 on the schematic)
        Connector("j", 0, " -  -  8  7 41 39 40  -  -  - 23 25 26 27 32 35 31 37 34 43 36 42 38 28"),
        # "Right" row of header pins (JP2 on the schematic)
        Connector("j", 1, "16 15 17 14 20 10  -  - 12 21 13 19 18 11  9  6 44  4  3 48 45 47 46  2")
    ]

    def toolchain_program(self, products, name):
        iceprog = os.environ.get("ICEPROG", "iceprog")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call([iceprog, bitstream_filename])

