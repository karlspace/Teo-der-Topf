# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

#######################################################################################################################
#
# Description :  Package for Toni der Topf
# Author      :  Karl Bauer (karl.bauer@bauer-group.com) / www.bauer-group.com
#
#######################################################################################################################

# System Imports
from datetime import datetime
import json
import paho.mqtt.client as mqtt

class TelemetryClient:
    def __init__(self, mqtt_server, base_topic, sensor_manager, username, password, mqtt_port=1883):
        self.mqtt_server = mqtt_server
        self.mqtt_port = mqtt_port
        self.base_topic = base_topic
        self.sensor_manager = sensor_manager

        # Create an MQTT client
        self.client = mqtt.Client()

        # Set username and password
        self.client.username_pw_set(username, password)

        # Connect to the MQTT server
        self.client.connect(self.mqtt_server, self.mqtt_port)

        # Set up subscriptions to sensor callbacks
        self.sensor_manager.subscribe_temperature(self.temperature_callback)
        self.sensor_manager.subscribe_pressure(self.pressure_callback)
        self.sensor_manager.subscribe_light_intensity(self.light_intensity_callback)
        self.sensor_manager.subscribe_ads1x15_channel_values(self.ads1x15_channel_values_callback)

    def temperature_callback(self, temperature):
        payload = json.dumps({
            "celsius": temperature,
            "timestamp": datetime.now().isoformat()
        })
        self.client.publish(f"{self.base_topic}/temperature", payload)

    def pressure_callback(self, pressure):
        payload = json.dumps({
            "hpa": pressure,
            "timestamp": datetime.now().isoformat()
        })
        self.client.publish(f"{self.base_topic}/pressure", payload)

    def light_intensity_callback(self, light_intensity):
        payload = json.dumps({
            "lux": light_intensity,
            "timestamp": datetime.now().isoformat()
        })
        self.client.publish(f"{self.base_topic}/light_intensity", payload)

    def ads1x15_channel_values_callback(self, ads1x15_channel_values):
        payload = json.dumps({
            "channel0": ads1x15_channel_values[0],
            "channel1": ads1x15_channel_values[1],
            "channel2": ads1x15_channel_values[2],
            "channel3": ads1x15_channel_values[3],
            "timestamp": datetime.now().isoformat()
        })
        self.client.publish(f"{self.base_topic}/ad_converter", payload)
