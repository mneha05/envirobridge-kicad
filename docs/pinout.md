# Connector pinout

Both J1 and J2 expose the same logical interface.

```text
Pin 1 — GND
Pin 2 — 3V3
Pin 3 — SDA
Pin 4 — SCL
```

For a NUCLEO-L476RG-style host, connect these nets to any configured 3.3 V I²C peripheral. Do not assume a specific Arduino-header I²C pin location without checking the exact Nucleo board revision/schematic.

## Address defaults

| Sensor | Strap | Default address |
|---|---|---|
| U1 | SDO → GND | 0x76 |
| U2 | SDO → 3V3 | 0x77 |
