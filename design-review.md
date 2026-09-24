# Design review — EnviroBridge

## Requirements translated into hardware

The board had five functional requirements:

1. expose two environmental sensors to one MCU over I²C;
2. avoid address collision between identical sensors;
3. work with either jumper wires or a compact keyed cable;
4. remain easy to debug on the bench;
5. be simple enough for a first fabrication run.

The design answers those requirements directly instead of adding features for their own sake.

## Schematic reasoning

### BME280 interface mode
BME280 supports SPI and I²C. The board uses I²C because the sensor node only needs four conductors and both devices can share SDA/SCL. `CSB` is tied high for I²C mode.

### Address selection
`SDO` selects the I²C address. Each sensor receives a 3-pad strap between GND and 3V3. The intended assembly defaults are U1=`0x76`, U2=`0x77`.

### Pull-ups
I²C requires pull-ups. 4.7 kΩ is a common starting point for a short 3.3 V sensor bus. The board makes the pull-ups disconnectable because the upstream MCU board may already populate them.

### Decoupling
Each IC gets 100 nF close to its supply pins. A 4.7 µF capacitor sits near the incoming 3.3 V connector. This is standard local decoupling and does not substitute for formal PDN analysis.

## Layout reasoning

### Sensor placement
The environmental sensors are intentionally near opposite edges. This improves ambient exposure and keeps them away from connector/body heat and concentrated digital activity.

### Grounding
The back layer is assigned primarily to GND. The design avoids chopping that plane with unnecessary signal routing.

### Trace strategy
- 3V3 is routed wider than SDA/SCL.
- SDA/SCL take direct, readable paths.
- no decorative serpentine routing or fake length matching is used because I²C at sensor-node speeds does not justify it.

### Test access
The bus and power rails have dedicated test pads. This is one of the most practical differences between a schematic-only design and a board designed for bring-up.

## What I would do before fabrication

- confirm BME280 land pattern against the latest Bosch datasheet;
- confirm J2 JST-SH pin orientation against the selected manufacturer part;
- run ERC and DRC in the target KiCad version;
- inspect 3D view for courtyard and connector-clearance issues;
- print the board at 1:1 scale and physically check connectors / mounting holes;
- generate Gerbers, drill files, and position/BOM outputs;
- inspect Gerbers in a separate viewer before ordering.

## What I would *not* claim from this board

- controlled-impedance routing;
- eye-diagram analysis;
- DDR / PCIe / RF design;
- formal signal-integrity simulation;
- formal power-integrity simulation.

This board is a compact low-speed mixed sensor interface and should be described that way.
