# RISE – Ground Control Station GUI

A desktop ground control application for monitoring the TINA_V1 rocket in real time. Built with PyQt5, it receives telemetry over LoRa radio and displays live flight data during launch.

<img width="1600" height="999" alt="gcs_gui" src="https://github.com/user-attachments/assets/bd0aa886-b866-4186-9a54-49df763885c7" />


---

## Features

- **Mission timer** — elapsed time since launch shown at the top (`T+HH:MM:SS`)
- **Acceleration plot** — live XYZ acceleration over time (m/s²)
- **Altitude plot** — barometer-derived altitude in km
- **Rocket orientation** — 3D visualisation of the rocket's attitude based on IMU data
- **Pyro channel status** — armed/fired state for all channels on both the Main and Redundant Flight Computers
- **Live data panel** — real-time readouts from both IMUs (roll, pitch, yaw, acceleration) and the barometer (pressure, altitude)
- **LoRa terminal** — scrollable timestamped log of incoming radio packets
- **Radio status** — RSSI and time since last message received
- **Arm / Deploy buttons** — arm the rocket and manually trigger parachute deployment

---

## Requirements

```
Python 3.x
PyQt5
pyserial
```

```bash
pip install PyQt5 pyserial
```

---

## Running

```bash
python main.py
```

The GCS reads packets over the serial port connected to the ground-side Wio-E5-LE LoRa module. Make sure the module is plugged in and on the correct COM port before starting.

---

## Project Structure

```
main.py              – entry point
MainWindow.py        – main layout, wires all widgets together
accelerationplot.py  – live acceleration graph
altitudeplot.py      – live altitude graph
orientation.py       – 3D rocket orientation widget
pyrochannels.py      – pyro channel status indicators
datadisplay.py       – live IMU + barometer readouts
armingswitches.py    – arm and deploy buttons
timer.py             – mission elapsed time display
```

---


