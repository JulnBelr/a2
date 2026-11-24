import network
from time import sleep

def connect_wifi(ssid, password, timeout=15):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        for _ in range(timeout * 2):
            if wlan.isconnected():
                break
            sleep(0.5)
    if not wlan.isconnected():
        raise RuntimeError("Wi-Fi connection failed")
    return wlan
