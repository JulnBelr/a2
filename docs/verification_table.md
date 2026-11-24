# Assignment 2 — Verification Table

**Team:** Julien Belanger & Adam Hamade  
**Station:** 2607  
**Pi Broker:** `192.168.0.172`

| R-ID | Requirement Summary | Concrete Check / Test Procedure | Evidence Kept | Status |
| :--- | :--- | :--- | :--- | :--- |
| **R-01** | Calibrated light sensing (`0–100%`) | Read sensor in dark & bright conditions; verify clamped `0.0–100.0%` | `docs/evidence/pid_disturbance_run.txt` | Demonstrated |
| **R-02** | Fixed-period control loop (`monotonic`) | Measure loop interval $\Delta t$ with `time.ticks_ms()`; verify steady `100 ms` period | `src/esp32/main.py` + telemetry log | Demonstrated |
| **R-03** | PID control law ($P$, $I$, $D$) & anti-windup | Step setpoint `50% -> 65%`; verify zero steady-state offset & clamped duty (`0–65535`) | `docs/evidence/pid_disturbance_run.txt` | Demonstrated |
| **R-04** | Disturbance rejection (shadow & uncover) | Shade LDR with hand, then uncover; verify PV returns to `65.0%` target | `docs/evidence/pid_disturbance_run.txt` | Demonstrated |
| **R-05** | MQTT telemetry & remote setpoint | Publish `65.0` to `bench/2607/setpoint`; verify live target update & JSON telemetry | `docs/evidence/pid_disturbance_run.txt` | Demonstrated |
| **R-06** | Last Will & clean offline status | Unplug ESP32 power; verify broker publishes retained `"offline"` to `bench/2607/status` | `docs/evidence/status_lwt_proof.txt` | Demonstrated |
