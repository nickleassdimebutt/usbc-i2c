"""usbc-i2c — orchestrator. Mirrors usbc-3v3 build.py but for the
single-cell Li-ion charger + 3.3V regulator board."""
import argparse
import sys
from pathlib import Path

import circuit
import layout
from circuit_toolkit.builders import build_pcb, build_schematic
from circuit_toolkit.fab import write_bom


PROJECT_DIR = Path(__file__).resolve().parent
PCB_PATH = PROJECT_DIR / "usbc-i2c.kicad_pcb"


def _parse_args(argv):
    p = argparse.ArgumentParser(description="usbc-i2c build orchestrator")
    p.add_argument("--datasheet", action="store_true",
                   help="render 3D PNGs and assemble the LT-style datasheet PDF")
    p.add_argument("--sim", action="store_true",
                   help="run SPICE pre-flight analyses (LDO operating point)")
    p.add_argument("--monte-carlo-runs", type=int, default=100)
    return p.parse_args(argv)


def main(argv=None):
    args = _parse_args(sys.argv[1:] if argv is None else argv)

    board = circuit.build()
    print(f"=== usbc-i2c build ({board}) ===\n")

    print(f"  → PCB: {PCB_PATH.name}")
    build_pcb(
        board,
        positions=layout.positions,
        output=PCB_PATH,
        tracks=layout.tracks,
        vias=layout.vias,
        zones=layout.zones,
        pad_zone_full=layout.pad_zone_full,
        ref_text_overrides=layout.ref_text_overrides,
        outline=layout.outline,
    )

    schematic_svg = PROJECT_DIR / "output/docs/schematic.svg"
    print(f"  → Schematic: {schematic_svg.relative_to(PROJECT_DIR)}")
    try:
        build_schematic(board, schematic_svg)
    except Exception as e:
        print(f"     [warning] schematic generation failed: {e}")

    print(f"  → BOM: output/fab/bom/")
    write_bom(board, PROJECT_DIR / "output/fab/bom")

    sim_dir = PROJECT_DIR / "output/sim"
    if args.sim:
        print(f"\n  → SPICE pre-flight: {sim_dir.relative_to(PROJECT_DIR)}/")
        from circuit_toolkit.sim import simulate_all
        # The board has BAT as the LDO's input rail (not VBUS), so the sim
        # framework's defaults need adjusting; passing vbus_net="BAT" makes
        # the test source drive BAT directly.
        try:
            paths = simulate_all(board, sim_dir,
                                 monte_carlo_runs=args.monte_carlo_runs)
            for name, p in paths.items():
                print(f"     {name:<14} {p.name}")
        except Exception as e:
            print(f"     [warning] sim failed: {e}")

    if args.datasheet:
        render_dir = PROJECT_DIR / "output/render"
        docs_dir = PROJECT_DIR / "output/docs"
        print(f"\n  → 3D renders + pcbdraw: {render_dir.relative_to(PROJECT_DIR)}/")
        from circuit_toolkit.builders import (
            render_pcb, build_datasheet, plot_pcbdraw,
            build_hierarchical_schematic,
        )
        render_pcb(PCB_PATH, render_dir, sides=("top", "bottom"))
        try:
            plot_pcbdraw(PCB_PATH, render_dir,
                         sides=("front", "back"), to_png=True, dpi=200)
            pcbdraw_front = render_dir / "pcbdraw_front.png"
            pcbdraw_back = render_dir / "pcbdraw_back.png"
        except Exception as e:
            print(f"     [warning] pcbdraw failed: {e}")
            pcbdraw_front = pcbdraw_back = None

        try:
            schematic_blocks = build_hierarchical_schematic(
                board, docs_dir / "hierarchical")
        except Exception as e:
            print(f"     [warning] hierarchical schematic failed: {e}")
            schematic_blocks = None

        pdf_path = docs_dir / "datasheet.pdf"
        print(f"  → Datasheet PDF: {pdf_path.relative_to(PROJECT_DIR)}")
        build_datasheet(
            board, pdf_path,
            rev="0.1",
            description="USB-C → 3.3 V → I²C breakout board",
            render_top=render_dir / "render_top.png",
            render_bottom=render_dir / "render_bottom.png",
            pcbdraw_front=pcbdraw_front,
            pcbdraw_back=pcbdraw_back,
            schematic_svg=schematic_svg,
            schematic_blocks=schematic_blocks,
            sim_dir=sim_dir if args.sim else None,
        )

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
