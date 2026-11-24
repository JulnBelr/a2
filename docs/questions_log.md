# Assignment 2 — Questions & Ambiguities Log

**Team:** Julien Belanger & Adam Hamade  
**Station:** 2607

| Date | Spec Reference / Topic | Ambiguity / Question | Resolution / Answer |
| :--- | :--- | :--- | :--- |
| 2026-10-28 | Control loop period ($\Delta t$) | Does the brief mandate a specific sample period (e.g., 50 ms vs. 100 ms) for the PID loop? | Defaulted to 100 ms (`0.1 s`) using monotonic ticks; easily configurable in `main.py`. |
| 2026-10-28 | Setpoint source | Should the setpoint start at a hardcoded boot default (e.g., `50.0%`) before any MQTT command arrives? | Yes—boot with `SP = 50.0` so standalone operation works immediately, and allow live updates over `bench/2607/setpoint`. |
| 2026-10-28 | Telemetry payload format | Should telemetry publish separate topics (`/light`, `/duty`, `/setpoint`) or a single JSON object? | Implemented JSON telemetry on `bench/2607/telemetry` (matching Week 9 Rung 4) plus individual topics if required. |
