# Bring-up checklist

## Before power

- [ ] Visually inspect U1/U2 orientation.
- [ ] Check resistance from 3V3 to GND; investigate an obvious short before powering.
- [ ] Confirm SJ1/SJ2 do not put both sensors on the same address.
- [ ] Confirm whether SJ3/SJ4 pull-ups should be enabled for the host board.

## First power

- [ ] Apply current-limited 3.3 V.
- [ ] Measure 3V3 at TP_3V3.
- [ ] Confirm GND continuity at TP_GND.
- [ ] Check that neither sensor becomes warm.

## I²C validation

- [ ] Scan bus; expect `0x76` and `0x77` with default straps.
- [ ] Probe SDA/SCL test points with a logic analyzer.
- [ ] Read BME280 chip ID (`0x60`) from both devices.
- [ ] Read temperature/pressure/humidity from both sensors.
- [ ] Compare readings at ambient conditions and note steady-state offset.

## Debug order if a sensor is missing

1. verify 3V3 at the device;
2. verify CSB is high;
3. verify SDO/address strap;
4. inspect SDA/SCL solder joints;
5. check whether pull-ups exist somewhere on the bus;
6. reduce bus speed;
7. probe transactions with a logic analyzer.
