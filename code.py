# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import wifi
import json
import socketpool
import time
import board
import scd4
import neopixel
import feathers3
from adafruit_minimqtt.adafruit_minimqtt import MQTT


def load_env(file_path=".env"):
    env_vars = {}
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip()
    return env_vars


env_vars = load_env()

# Initialize the os variables
WIFI_SSID = env_vars.get("WIFI_SSID")
PW = env_vars.get("PW")
MQTT_BROKER = env_vars.get("MQTT_BROKER")
MQTT_PORT = int(env_vars.get("MQTT_PORT"))
MQTT_TOPIC_CO2 = env_vars.get("MQTT_TOPIC_CO2")
MQTT_TOPIC_TEMP = env_vars.get("MQTT_TOPIC_TEMP")
MQTT_TOPIC_HUMID = env_vars.get("MQTT_TOPIC_HUMID")
try:
    wifi.radio.connect(WIFI_SSID, PW)
    print(f"Connected to WIFI {WIFI_SSID}")
except Exception as e:
    print("Failed to connect to WIFI!", e)


class SocketPoolWrapper:
    def __init__(self, socket_pool):
        self.socket_pool = socket_pool

    def __hash__(self):
        return hash(id(self.socket_pool))

    def __eq__(self, other):
        return isinstance(other, SocketPoolWrapper) and id(self.socket_pool) == id(
            other.socket_pool
        )

    def __getattr__(self, name):
        # Forward all other attribute access to the original socket_pool object
        return getattr(self.socket_pool, name)


# pool = socketpool.SocketPool(wifi.radio)
# pool = SocketPoolWrapper(pool)
#
# mqtt_client = MQTT(
#     broker=MQTT_BROKER,
#     port=MQTT_PORT,
#     socket_pool=pool,
#     socket_timeout=5,
# )
# mqtt_client.connect()
# print("success")


pixel = neopixel.NeoPixel(
    board.NEOPIXEL, 1, brightness=0.3, auto_write=True, pixel_order="GRB"
)
device = scd4.SCD4X(quiet=False)
device.start_periodic_measurement()
color_index = 0

# Turn on the power to the NeoPixel
feathers3.set_ldo2_power(True)


def get_rgb_values(co2):
    if co2 < 800:
        return (255, 0, 0)
    elif co2 >= 800 and co2 < 1200:
        return (255, 255, 0)
    else:
        return (0, 255, 0)


while True:
    time.sleep(15)
    try:
        co2, temperature, relative_humidity, timestamp = device.measure()
        print(
            f"co2:{co2} ppm, T:{temperature} C, humid: {relative_humidity} %, timestamp: {timestamp} ms"
        )
        co2_payload = json.dumps({"value": co2, "unit": "ppm", "timestamp": timestamp})
        temp_payload = json.dumps(
            {"value": temperature, "C": "ppm", "timestamp": timestamp}
        )
        humid_payload = json.dumps(
            {"value": relative_humidity, "unit": "ppm", "timestamp": timestamp}
        )
        # mqtt_client.publish(MQTT_TOPIC_CO2, co2_payload)
        # mqtt_client.publish(MQTT_TOPIC_TEMP, temp_payload)
        # mqtt_client.publish(MQTT_TOPIC_HUMID, humid_payload)

        while True:
            time.sleep(15)
            try:
                co2, temperature, relative_humidity, timestamp = device.measure()
                print(
                    f"co2:{co2} ppm, T:{temperature} C, humid: {relative_humidity} %, timestamp: {timestamp} ms"
                )
                co2_payload = json.dumps(
                    {"value": co2, "unit": "ppm", "timestamp": timestamp}
                )
                temp_payload = json.dumps(
                    {"value": temperature, "C": "ppm", "timestamp": timestamp}
                )
                humid_payload = json.dumps(
                    {"value": relative_humidity, "unit": "ppm", "timestamp": timestamp}
                )
                # mqtt_client.publish(MQTT_TOPIC_CO2, co2_payload)
                # mqtt_client.publish(MQTT_TOPIC_TEMP, temp_payload)
                # mqtt_client.publish(MQTT_TOPIC_HUMID, humid_payload)

                G, R, B = get_rgb_values(co2)
                pixel[0] = (G, R, B, 0.5)

                feathers3.led_blink

                # mqtt_client.loop(timeout=10)

            except Exception as e:
                print(f"ERROR - {e}")
                print("Attempting to reconnect...")

        # mqtt_client.loop(timeout=10)

    except Exception as e:
        print(f"ERROR - {e}")
        print("Attempting to reconnect...")
