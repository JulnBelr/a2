import csv
import json
import time
import threading
import paho.mqtt.client as mqtt

BROKER  = "localhost"
STATION = "2607"

TOPIC_TELEM  = f"bench/{STATION}/telemetry"
TOPIC_SP     = f"bench/{STATION}/setpoint"
TOPIC_TUNING = f"bench/{STATION}/tuning"
CSV_FILE     = f"a2_log_{STATION}.csv"

with open(CSV_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "sp", "pv", "err", "duty"])

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to broker:", reason_code)
    client.subscribe(TOPIC_TELEM)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    ts = round(time.monotonic(), 2)
    print(f"SP: {data['sp']:5.1f}% | PV: {data['pv']:5.1f}% | Err: {data['err']:+5.1f}% | Duty: {data['duty']:5d}")
    with open(CSV_FILE, "a", newline="") as f:
        csv.writer(f).writerow([ts, data["sp"], data["pv"], data["err"], data["duty"]])

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883)
client.loop_start()

print("Commands: enter a number (0-100) to set target %, or 'q' to quit.")
try:
    while True:
        cmd = input().strip()
        if cmd.lower() == "q":
            break
        try:
            val = float(cmd)
            client.publish(TOPIC_SP, str(val))
            print(f"--> Sent new setpoint: {val}%")
        except ValueError:
            print("Enter a number between 0 and 100, or 'q'.")
finally:
    client.loop_stop()
    client.disconnect()
