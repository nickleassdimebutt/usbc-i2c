# usbc-i2c

USB-C powered I²C breakout — 5 V in, 3.3 V out, 10 kΩ SDA/SCL pullups,
4-pin header to chain sensors. Power-good LED (green) on +3V3.

PCBA-2 test project for the [kicad-claude-toolkit](https://github.com/nickleassdimebutt/kicad-claude-toolkit)
v3 toolchain. Tighter layout than usbc-charger (14 components vs 23) so
hand-routed tracks could go DRC-clean for the routing that *does* exist.

## Layout status

The validated routes from usbc-3v3 (J1 escape, VBUS bus, CC pulldowns,
GND bridges) are reused verbatim. The new fan-out (+3V3 to LDO output
caps, the I²C pullups, the LED, the 4-pin user header) is left for
KiCad GUI hand-routing — same reason as usbc-charger: code-only routing
without a visual feedback loop accumulates pad-coordinate errors very
quickly.

DRC reports:

- 10 unconnected items — every +3V3 / SDA / SCL / N_D1 stub (expected,
  routing TODO)
- 1 dangling track — leftover endpoint from a stub I trimmed
- 4 cosmetic silk warnings (overlap, edge clearance, copper clip) — all
  non-fatal, would be silenced via project rule overrides

The board is **topologically correct** (`circuit.py` builds, BOM is
clean, schematic SVG renders) and the full datasheet pipeline runs
end-to-end on it.

## Build

```powershell
& "C:\Program Files\KiCad\10.0\bin\python.exe" build.py --datasheet --sim
```

## Topology summary

| Block | Components | Function |
|-------|------------|----------|
| `usbc_power` | J1 + R1, R2 | USB-C 5 V input + CC pulldowns |
| `ldo` | U1 + C1, C2, C3 | AMS1117-3.3 LDO with bypass caps |
| `i2c_pullups` | R10, R11 | 10 kΩ SDA / SCL pullups to +3V3 |
| `led` | D1 + R3 | Green +3V3 power-good indicator |
| `header` | J2 | 4-pin I²C user header (3V3/GND/SDA/SCL) |
| `mounting` | H1, H2 | Two M2 corner holes |

14 components, 8 nets, 50 × 30 mm.
