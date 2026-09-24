# EnviroBridge — Dual BME280 Sensor Daughterboard

A compact 2-layer KiCad sensor board for an STM32-class sensor node. The board carries **two bare BME280 environmental sensors** on one I²C bus, with independent address selection, optional local pull-ups, test access, dual connector options, and deliberate sensor placement near the PCB edge for airflow.

> This repository demonstrates practical PCB-design exposure: schematic capture, component selection, footprint/layout work, routing, decoupling, connector planning, address configuration, testability, silkscreen/documentation, and fabrication handoff. It does **not** claim high-speed signal-integrity or power-integrity analysis.

## Board at a glance

```text
             airflow                         airflow
                ↓                               ↓
   ┌───────────────────────────────────────────────────┐
   │  TP_SDA  TP_SCL  TP_3V3  TP_GND                  │
   │                                                   │
   │  U1 BME280                         U2 BME280       │
   │  default 0x76                     default 0x77     │
   │     │                                 │           │
   │   C1 100n                           C2 100n        │
   │                                                   │
   │          R1/R2 4.7k I²C pull-ups                 │
   │          SJ3/SJ4 enable/disable                  │
   │                                                   │
   │  J2 Qwiic/JST-SH       J1 2.54 mm header         │
   │  GND 3V3 SDA SCL       GND 3V3 SDA SCL           │
   └───────────────────────────────────────────────────┘
       M2.5                                      M2.5
```

## Why two sensors?

BME280 supports two I²C addresses through the SDO pin. EnviroBridge uses that intentionally:

- **U1 default:** `0x76`
- **U2 default:** `0x77`
- each device has a **3-pad address solder jumper** so the address can be changed during bring-up

This is useful for validating sensor agreement, experimenting with sensor placement, or collecting redundant environmental readings without adding an I²C mux.

## Design choices

### 1. Sensors are on opposite board edges
Humidity/temperature sensors should not be buried next to warm regulators or dense digital logic. U1 and U2 sit near opposite edges with a keep-clear area around them so they are exposed to ambient air rather than a local board hot spot.

### 2. Local decoupling is physically close
Each BME280 has a dedicated **100 nF ceramic capacitor** close to VDD/VDDIO. A **4.7 µF bulk capacitor** is placed near the connector entry point.

This is ordinary decoupling practice—not a claim that the board has undergone power-integrity simulation.

### 3. I²C pull-ups are present but configurable
R1/R2 are 4.7 kΩ pull-ups to 3.3 V. SJ3/SJ4 make them optional so the board can be attached to a bus that already has pull-ups without blindly stacking another pair.

### 4. Two connector styles
- **J1:** 1×4, 2.54 mm header for bench work / jumper wires
- **J2:** JST-SH 4-pin Qwiic-style connector for compact sensor-node wiring

Both expose the same four nets: `GND`, `3V3`, `SDA`, `SCL`.

### 5. Testability is designed in
Dedicated pads for `3V3`, `GND`, `SDA`, and `SCL` make it possible to probe power and the bus with a multimeter, oscilloscope, or logic analyzer without clipping onto tiny LGA pads.

### 6. Simple 2-layer stackup
- **F.Cu:** component placement + most routing
- **B.Cu:** ground plane
- wide 3.3 V distribution relative to I²C traces
- no unnecessary layer changes on the bus

Again, this is layout hygiene—not high-speed SI/PI engineering.

## Repository structure

```text
envirobridge-kicad/
├── EnviroBridge.sch             # KiCad legacy schematic source (importable by current KiCad)
├── EnviroBridge.kicad_pcb       # routed 2-layer PCB
├── EnviroBridge.kicad_pro       # project metadata
├── EnviroBridge.kicad_dru       # basic board constraints
├── bom.csv                      # concise BOM
├── design-review.md             # design rationale + interview walkthrough
├── bringup-checklist.md         # first-power / I²C validation steps
├── docs/
│   └── pinout.md
└── fabrication/
    └── fab-notes.md
```

## Pinout

| Pin | Net | Purpose |
|---|---|---|
| 1 | GND | Ground |
| 2 | 3V3 | 3.3 V input |
| 3 | SDA | I²C data |
| 4 | SCL | I²C clock |

## BOM summary

| Ref | Part | Value / role |
|---|---|---|
| U1, U2 | Bosch BME280 | temp / humidity / pressure sensor |
| C1, C2 | 0402 ceramic | 100 nF local decoupling |
| C3 | 0603/0805 ceramic | 4.7 µF input bulk |
| R1, R2 | 0402 resistor | 4.7 kΩ I²C pull-ups |
| SJ1, SJ2 | 3-pad solder jumper | BME280 address select |
| SJ3, SJ4 | 2-pad solder jumper | pull-up enable |
| J1 | 1×4 header | bench/debug connection |
| J2 | JST-SH 4-pin | compact sensor-node connection |
| TP1–TP4 | test point | 3V3/GND/SDA/SCL |

## Opening the project

1. Open `EnviroBridge.kicad_pcb` in KiCad PCB Editor.
2. Open `EnviroBridge.sch` in Schematic Editor; current KiCad versions can import the legacy schematic format and save it as `.kicad_sch`.
3. Run **Inspect → Design Rules Checker** after import.
4. Re-associate any library symbols/footprints if your KiCad installation uses different library names.

The PCB file embeds the actual custom pad geometry for the key footprints, so the physical layout does not depend on an external custom-footprint library.

## What to talk through in an interview

Open the board and explain the path in this order:

1. connector brings in `3V3/GND/SDA/SCL`;
2. bulk cap handles local load transients at board entry;
3. optional I²C pull-ups sit near the connector side of the bus;
4. SDA/SCL fan out to both BME280s;
5. the two address straps keep both sensors usable on one bus;
6. each sensor gets local 100 nF decoupling;
7. test points make bring-up/debugging easier;
8. sensors are placed at the board edges for better ambient exposure;
9. B.Cu is used as a continuous ground plane wherever possible.

That is enough to demonstrate that you can reason about a small board from **electrical requirements → schematic → placement → routing → bring-up**, without pretending it is a high-speed board.
