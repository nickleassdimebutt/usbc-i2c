"""USB-C → 3.3V → I²C breakout board.

PCBA-2 test project for the circuit_toolkit. A USB-C-powered I²C bus
breakout: USB-C in, AMS1117-3.3 LDO, two 10 kΩ pull-ups on SDA/SCL,
power-good LED, and a 4-pin user header (3V3/GND/SDA/SCL) for chaining
sensors.

Smaller and tighter than usbc-3v3 (12 components vs 15) so the
hand-routed layout has a chance of going DRC-clean without GUI iteration.
"""
from circuit_toolkit import Board
from circuit_toolkit.blocks import (
    usbc_power, ams1117_ldo, led_indicator, pin_header, m2_mounting_hole,
    block_scope,
)
from circuit_toolkit.core.component import Component


def build() -> Board:
    board = Board("usbc-i2c", size=(50, 30))

    # USB-C input
    vbus, gnd, _, _ = usbc_power(board, ref="J1", cc_pulldowns="5.1k")

    # 3.3V LDO
    v3v3 = ams1117_ldo(
        board, ref="U1",
        vin=vbus, gnd=gnd, output_voltage=3.3,
        in_caps=["10uF/0805"],
        out_caps=["10uF/0805", "100nF/0402"],
    )

    # I²C signals + 10k pull-ups to V_3V3
    sda = board.net("SDA")
    scl = board.net("SCL")

    with block_scope(board, "i2c_pullups"):
        for ref, net in (("R10", sda), ("R11", scl)):
            r = Component(
                ref=ref,
                value="10k",
                footprint="Resistor_SMD:R_0402_1005Metric",
                lcsc="C25744", lcsc_basic=True,        # 10 kΩ 0402 1 % JLC basic
                pin_map={"1": "1", "2": "2"},
                description="Resistor 10k 0402 (I²C pull-up)",
            )
            board.add(r)
            board.connect(v3v3, r, "1")
            board.connect(net,  r, "2")

    # Power-good LED on +3V3
    led_indicator(
        board, ref_led="D1", ref_resistor="R3",
        vin=v3v3, gnd=gnd, color="green", current_ma=1.3,
        supply_voltage=3.3,
    )

    # 4-pin I²C header (+3V3, GND, SDA, SCL)
    pin_header(board, ref="J2", pins=4, label="I2C",
               nets=[v3v3, gnd, sda, scl])

    # Two M2 mounting holes (smaller board → 2 instead of 4)
    m2_mounting_hole(board, ref="H1")
    m2_mounting_hole(board, ref="H2")

    return board


if __name__ == "__main__":
    b = build()
    print(b)
    for c in b.components:
        print(f"  {c.ref:<5} {c.value:<25}  {c.block_id}")
