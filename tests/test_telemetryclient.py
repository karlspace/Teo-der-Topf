from unittest.mock import patch
from pathlib import Path
import sys
import json

import paho.mqtt.client as mqtt

root_path = Path(__file__).resolve().parents[1]
sys.path.append(str(root_path))

from Application.telemetryclient import TelemetryClient


class DummyClient:
    def __init__(self):
        self.published = []

    def username_pw_set(self, username, password):
        pass

    def connect(self, server, port):
        pass

    def publish(self, topic, payload):
        self.published.append((topic, payload))


class DummySensorManager:
    def __init__(self):
        self.callbacks = []
        self.temperature = 22.5
        self.pressure = 1000.5
        self.light_intensity = 50
        self.ads1x15_channel_values = [1, 2, 3, 4]

    def register_callback(self, callback):
        self.callbacks.append(callback)


@patch.object(mqtt, "Client", return_value=DummyClient())
def test_telemetryclient_publish_topics(_):
    sensor_manager = DummySensorManager()
    client = TelemetryClient("localhost", "teo", sensor_manager, "user", "pwd")

    client.temperature_callback(sensor_manager)
    client.pressure_callback(sensor_manager)
    client.light_intensity_callback(sensor_manager)
    client.ads1x15_channel_values_callback(sensor_manager)

    topics = [t for (t, _) in client.client.published]
    assert topics == [
        "teo/temperature",
        "teo/pressure",
        "teo/light_intensity",
        "teo/ad_converter",
    ]

    payload = json.loads(client.client.published[0][1])
    assert payload["celsius"] == sensor_manager.temperature
    assert "timestamp" in payload

