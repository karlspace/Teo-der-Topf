from unittest.mock import patch
from pathlib import Path
import sys
import types

import paho.mqtt.client as mqtt

root_path = Path(__file__).resolve().parents[1]
sys.path.append(str(root_path))

# Provide a minimal stub for SensorManager to avoid hardware imports
sensor_manager_module = types.ModuleType("Application.sensormanager")

class SensorManager:  # pragma: no cover - simple stub
    pass

sensor_manager_module.SensorManager = SensorManager
sys.modules["Application.sensormanager"] = sensor_manager_module

from Application.homeassistantsensor import HomeAssistantSensor
from Application.configuration import Configuration
from Application.applogger import ApplicationLogger


class DummyClient:
    def __init__(self, client_id):
        self.on_connect = None
        self.on_disconnect = None
        self.published = []

    def username_pw_set(self, username, password):
        pass

    def connect_async(self, server):
        pass

    def loop_start(self):
        pass

    def publish(self, topic, payload, retain=False):
        self.published.append((topic, payload, retain))

    def disconnect(self):
        pass

    def loop_stop(self):
        pass


class DummySensorManager:
    temperature = 21.5
    pressure = 1005
    light_intensity = 123
    ads1x15_channel_values = [12000, None, 15000, 16000]


@patch.object(mqtt, "Client", DummyClient)
def test_conversion_soil_moisture_none():
    config = Configuration()
    logger = ApplicationLogger(level=0)
    sensor = HomeAssistantSensor("localhost", "id", "user", "pwd", None, logger, config)
    assert sensor._conversion_soil_moisture(None) is None


@patch.object(mqtt, "Client", DummyClient)
def test_sensor_manager_callback_skips_none():
    config = Configuration()
    logger = ApplicationLogger(level=0)
    sensor = HomeAssistantSensor("localhost", "id", "user", "pwd", None, logger, config)
    dummy_manager = DummySensorManager()

    sensor._client.published.clear()
    sensor._HomeAssistantSensor__sensor_manager_callback(dummy_manager)

    topics = [t for (t, _, _) in sensor._client.published]
    skipped_topic = f"{sensor._base_topic}/sensor/{sensor._client_id}/ad-channel1/state"
    assert skipped_topic not in topics
