import json
import time
from umqtt.simple import MQTTClient
import config
from net import connect_wifi
from lightnode import LightNode
from pid import PID

TOPIC_TELEM  = f"bench/{config.STATION}/telemetry".encode()
TOPIC_STATUS = f"bench/{config.STATION}/status".encode()
TOPIC_SP     = f"bench/{config.STATION}/setpoint".encode()
TOPIC_TUNING = f"bench/{config.STATION}/tuning".encode()

LOOP_MS    = 100   # 10 Hz PID update rate
PUBLISH_MS = 500   # 2 Hz MQTT telemetry rate

state = {
    "setpoint": 50.0,
    "mode": "auto"  # "auto" (PID) or "manual"
}

connect_wifi(config.WIFI_SSID, config.WIFI_PASSWORD)

# Update dark/bright with your station's Week 8 calibration anchors
node = LightNode(adc_pin=34, pwm_pin=25, dark=200, bright=3550)

# Initial PID gains (tune on your bench: start with Kp, add Ki, then small Kd)
pid = PID(kp=650.0, ki=300.0, kd=25.0, out_min=0, out_max=65535)

def on_msg(topic, msg):
    text = msg.decode().strip()
    if topic == TOPIC_SP:
        try:
            sp = max(0.0, min(100.0, float(text)))
            state["setpoint"] = sp
            state["mode"] = "auto"
            print("New setpoint:", sp)
        except ValueError:
            pass
    elif topic == TOPIC_TUNING:
        # Optional live tuning via JSON: {"kp": 700, "ki": 350, "kd": 20}
        try:
            data = json.loads(text)
            pid.kp = float(data.get("kp", pid.kp))
            pid.ki = float(data.get("ki", pid.ki))
            pid.kd = float(data.get("kd", pid.kd))
            pid.reset()
            print("Updated PID:", pid.kp, pid.ki, pid.kd)
        except Exception:
            pass

client = MQTTClient(f"a2-node-{config.STATION}", config.BROKER_IP, keepalive=30)
client.set_last_will(TOPIC_STATUS, b"offline", retain=True)
client.set_callback(on_msg)
client.connect()
client.publish(TOPIC_STATUS, b"online", retain=True)
client.subscribe(TOPIC_SP)
client.subscribe(TOPIC_TUNING)

last_ctrl = time.ticks_ms()
last_pub  = last_ctrl
duty = 0

while True:
    now = time.ticks_ms()
    dt_ms = time.ticks_diff(now, last_ctrl)

    if dt_ms >= LOOP_MS:
        dt = dt_ms / 1000.0
        last_ctrl = now

        pv = node.read_pct()
        sp = state["setpoint"]
        u = pid.update(sp, pv, dt)
        duty = node.set_duty(u)

        client.check_msg()

        if time.ticks_diff(now, last_pub) >= PUBLISH_MS:
            last_pub = now
            payload = json.dumps({
                "station": config.STATION,
                "sp": round(sp, 1),
                "pv": round(pv, 1),
                "err": round(sp - pv, 1),
                "duty": duty
            })
            client.publish(TOPIC_TELEM, payload.encode())

    time.sleep_ms(5)
