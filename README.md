# Assignment 2 — Closed-Loop PID Light Controller

**Course:** 420-302-VA — Internet of Things (Fall 2026)  
**Team:** Julien Belanger & Adam Hamade  
**Station:** 2607  
**Raspberry Pi Broker IP:** `192.168.0.172`

---

## Overview

This repository contains the firmware, Raspberry Pi telemetry/control scripts, and verification documentation for a **closed-loop PID light-harvesting controller**. An ESP32 reads calibrated ambient light percentage from an LDR voltage divider, computes a discrete PID control law at a fixed 100 ms monotonic loop period, and drives an LED via PWM to maintain a target light setpoint despite external disturbances (shadows or bright light). The node publishes real-time telemetry and accepts live setpoint updates over MQTT via a Mosquitto broker running on the Raspberry Pi.

---

## Hardware & Wiring

### Bill of Materials
* 1 × ESP32 Development Board
* 1 × Raspberry Pi (running Mosquitto MQTT broker)
* 1 × Photoresistor (LDR)
* 1 × 10 kΩ Resistor (for LDR voltage divider)
* 1 × LED (actuator light source)
* 1 × 330 Ω Resistor (LED current-limiting resistor)
* Breadboard and jumper wires

### ESP32 Pinout & Breadboard Connections

| Component | Circuit Connection | ESP32 Pin | Notes |
| :--- | :--- | :--- | :--- |
| **LDR Voltage Divider (Top)** | LDR Leg 1 → `3.3V` | `3V3` | Powers the light-sensing divider |
| **LDR Voltage Divider (Midpoint)** | LDR Leg 2 + 10 kΩ Leg 1 → Sense Node | `GPIO 34` | `ADC1_CH6` (`ATTN_11DB`, `0–3.3 V` input) |
| **LDR Voltage Divider (Bottom)** | 10 kΩ Leg 2 → Ground | `GND` | Pull-down resistor to ground |
| **Actuator LED (Anode / Long Leg)** | `GPIO 25` → 330 Ω Resistor → LED Anode | `GPIO 25` | `PWM` output (`1000 Hz`, `0–65535` duty) |
| **Actuator LED (Cathode / Short Leg)** | LED Cathode → Ground | `GND` | Common ground |

*Optical coupling note:* Position the actuator LED and LDR facing each other (or inside a small light-shielded tube/hood) on the breadboard so PWM duty changes directly register on the LDR while still allowing hand-shadow disturbance tests.

### Raspberry Pi Setup
* Connected to the same local Wi-Fi/LAN (`192.168.0.172`).
* Runs the Mosquitto MQTT broker listening on TCP port `1883` (`listener 1883`, `allow_anonymous true`).

---

## Repository Structure

```text
IOT-A2/
├── .gitignore
├── README.md
├── docs/
│   ├── verification_table.md       # Requirement-by-requirement test matrix & status
│   ├── questions_log.md            # Spec ambiguities and design resolutions
│   └── evidence/                   # Logged telemetry runs, LWT proof, and bench photos
└── src/
    ├── esp32/
    │   ├── config_example.py       # Template for Wi-Fi and broker settings
    │   ├── net.py                  # Wi-Fi station connection helper
    │   ├── lightnode.py            # Calibrated ADC sensor & PWM actuator class
    │   ├── pid.py                  # Discrete PID controller with anti-windup
    │   └── main.py                 # 10 Hz monotonic control loop & MQTT client
    └── pi/
        └── a2_dashboard.py         # Pi telemetry subscriber, CSV logger & setpoint CLI

---

## Control Loop & Calibration Parameters

* **Sensor Calibration (`LightNode`):**
  * Dark anchor (`0%`): `200` raw ADC *(update with your bench value)*
  * Bright anchor (`100%`): `3550` raw ADC *(update with your bench value)*
  * Sample averaging: `n = 10` samples per reading to reduce derivative noise
* **Monotonic Timing:** Fixed `100 ms` (`10 Hz`) control loop using `time.ticks_ms()` / `time.ticks_diff()`
* **Tuned PID Gains:** `Kp = 650.0`, `Ki = 300.0`, `Kd = 25.0` *(update with your final tuned gains)*
* **Sign Convention & Safety:** Error is defined as $e = SP - PV$ (positive error increases LED PWM duty; negative error decreases duty). Output is clamped to `[0, 65535]` with conditional integral clamping to prevent windup during actuator saturation.

---

## Team Workflow & Roles

* **Partners:** Julien Belanger & Adam Hamade
* **Protocol:** Driver / Navigator pair workflow with incremental commits tied directly to `docs/verification_table.md` and timestamped evidence in `docs/evidence/`.
* **Spec Governance:** All pin assignments, topic names, and deliverable thresholds follow the authoritative Omnivox Assignment 2 brief (see [`docs/questions_log.md`](docs/questions_log.md) for logged clarifications).
