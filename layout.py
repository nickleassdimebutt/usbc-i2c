"""usbc-i2c layout — adapts the proven usbc-3v3 placement to a slightly
wider 50×30 board so the 4-pin I²C header and two pullups fit without
crowding the LDO output area."""

# Components placed on a 50×30 mm board. Coordinates mirror usbc-3v3 for
# the parts they share (J1, U1, R1, R2, C1–C3, D1, R3, H1–H4) so the
# same routing strategy carries over.
positions = {
    # USB-C input (vertical)
    "J1": (5.5, 15, 270),
    "R1": (9, 8.5, 0),
    "R2": (9, 21.5, 0),

    # AMS1117 LDO + caps  (1 input cap, 2 output caps per circuit.py)
    "U1": (22, 15, 270),
    "C1": (13, 15, 0),       # 10uF VBUS input bypass
    "C2": (30, 10.5, 0),     # 10uF +3V3 output
    "C3": (30, 19.5, 0),     # 100nF +3V3 output

    # I²C pull-ups (10k each)
    "R10": (38, 8.5, 0),     # SDA pull-up
    "R11": (38, 12.5, 0),    # SCL pull-up

    # Power-good green LED
    "D1": (32, 21, 0),
    "R3": (37, 21, 0),

    # 4-pin I²C user header
    "J2": (45, 15, 0),

    # Mounting holes — opposite corners (saves space vs four)
    "H1": (3, 3, 0),
    "H2": (47, 27, 0),
}

ref_text_overrides = {}
pad_zone_full = [
    ("J1", "B7"), ("J1", "A8"),  # mirror usbc-3v3 zone-relief overrides
]

# Reuse usbc-3v3's tested track set verbatim for the J1↔R1/R2 + VBUS + GND
# bridges; add new short stubs for I²C pullups and the LED.
tracks = [
    # Validated tracks ported verbatim from usbc-3v3 (the J1 escape, VBUS bus,
    # CC pulldown routing, GND bridges). The +3V3 / SDA / SCL fan-out and the
    # LED stub are deferred to KiCad GUI hand-routing — see README.

    # VBUS rail
    ("VBUS", 9.545, 12.55, 11.8, 12.55, 0.3, "F.Cu"),
    ("VBUS", 9.545, 17.45, 11.8, 17.45, 0.3, "F.Cu"),
    ("VBUS", 11.8, 10.5, 11.8, 19.5, 0.5, "F.Cu"),
    ("VBUS", 11.8, 11.85, 19.7, 11.85, 0.8, "F.Cu"),

    # CC pulldowns — J1 → R1/R2 (B.Cu hop, vias)
    ("CC1", 9.545, 13.75, 10.87, 13.75, 0.3, "F.Cu"),
    ("CC1", 10.87, 13.75, 7.0, 13.75, 0.3, "B.Cu"),
    ("CC1", 7.0, 13.75, 7.0, 8.5, 0.3, "B.Cu"),
    ("CC1", 7.0, 8.5, 8.49, 8.5, 0.3, "F.Cu"),

    ("CC2", 9.545, 16.75, 10.87, 16.75, 0.3, "F.Cu"),
    ("CC2", 10.87, 16.75, 10.87, 16.0, 0.3, "F.Cu"),
    ("CC2", 10.87, 16.0, 7.0, 16.0, 0.3, "B.Cu"),
    ("CC2", 7.0, 16.0, 7.0, 21.5, 0.3, "B.Cu"),
    ("CC2", 7.0, 21.5, 8.49, 21.5, 0.3, "F.Cu"),

    # GND bridges — isolated J1 pads the zone can't reach
    ("GND", 9.545, 13.25, 7.5, 13.25, 0.25, "F.Cu"),
    ("GND", 9.545, 14.25, 7.5, 14.25, 0.25, "F.Cu"),
    ("GND", 9.545, 16.25, 7.5, 16.25, 0.25, "F.Cu"),
    ("GND", 8.63, 10.68, 9.545, 10.68, 0.25, "F.Cu"),
    ("GND", 9.545, 10.68, 9.545, 11.75, 0.25, "F.Cu"),
    ("GND", 8.63, 19.32, 9.545, 19.32, 0.25, "F.Cu"),
    ("GND", 9.545, 19.32, 9.545, 18.25, 0.25, "F.Cu"),
]

vias = [
    ("CC1", 10.87, 13.75, 0.4, 0.8),
    ("CC1", 7.0, 8.5, 0.4, 0.8),
    ("CC2", 10.87, 16.0, 0.4, 0.8),
    ("CC2", 7.0, 21.5, 0.4, 0.8),
]

zones = [
    {"net": "GND", "layer": "F.Cu",
     "polygon": [(1, 1), (49, 1), (49, 29), (1, 29)],
     "min_thickness": 0.25, "pad_connection": "thermal"},
]

outline = {"shape": "rect", "x": 0.0, "y": 0.0, "w": 50.0, "h": 30.0}
