# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

#######################################################################################################################
#
# Description :  Package for Toni der Topf
# Author      :  Karl Bauer (karl.bauer@bauer-group.com) / www.bauer-group.com
#
#######################################################################################################################

# System Imports
import json
import paho.mqtt.client as mqtt
import uuid

# Local Imports
from .sensormanager import SensorManager
from .applogger import ApplicationLogger
from .configuration import Configuration

class HomeAssistantSensor:
    def __init__(self, mqtt_server, ha_id, username, password, sensor_manager: SensorManager, app_logger: ApplicationLogger, config: Configuration):
        self._mqtt_server = mqtt_server
        #self._client_id = str(uuid.uuid4())
        self._client_id = ha_id
        self._base_topic = f"homeassistant"
        self._sensor_manager = sensor_manager
        self._log = app_logger
        self._config = config

        # Create an MQTT client
        self._client = mqtt.Client(self._client_id)

        # Set username and password
        self._client.username_pw_set(username, password)

        # Set up MQTT client callbacks
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect

        self._is_subscribed = False
        self._is_registered = False

        # Connect to the MQTT server
        self._client.connect_async(self._mqtt_server)

        # Start the MQTT loop
        self._client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self._log.info("HomeAssistant - Connected to MQTT broker successfully")
        else:
            self._log.error(f"HomeAssistant - Connection to MQTT broker failed with error code: {rc}")

        # Register the device only once
        if not self._is_registered:
            self._register_device()
            self._is_registered = True

        # Set up subscriptions to sensor callbacks only once
        if not self._is_subscribed:
            self._sensor_manager.register_callback(self.__sensor_manager_callback)
            self._is_subscribed = True

    def _on_disconnect(self, client, userdata, rc):
        if rc != mqtt.MQTT_ERR_SUCCESS:

            disconnect_reasons = {
                mqtt.MQTT_ERR_NOMEM: "Out of memory.",
                mqtt.MQTT_ERR_PROTOCOL: "A network protocol error occurred when communicating with the broker.",
                mqtt.MQTT_ERR_INVAL: "Invalid arguments were passed to a function.",
                mqtt.MQTT_ERR_NO_CONN: "The client is not currently connected.",
                mqtt.MQTT_ERR_CONN_REFUSED: "The server has refused the connection from the client.",
                mqtt.MQTT_ERR_CONN_LOST: "The connection was lost.",
                mqtt.MQTT_ERR_TLS: "A TLS error occurred.",
                mqtt.MQTT_ERR_PAYLOAD_SIZE: "Payload is too large.",
                mqtt.MQTT_ERR_NOT_SUPPORTED: "This feature is not supported.",
                mqtt.MQTT_ERR_AUTH: "Authorization failed.",
                mqtt.MQTT_ERR_ACL_DENIED: "Access denied by ACL.",
                mqtt.MQTT_ERR_UNKNOWN: "Unknown error.",
                mqtt.MQTT_ERR_ERRNO: "Check 'errno' for the error number."
            }

            reason = disconnect_reasons.get(rc, "Unknown reason.")
            self._log.warning(f"HomeAssistant - Unexpected disconnection: {reason} Reconnecting...")

    def _register_device(self):
        # Basic device information
        device_info = {
            "identifiers": [self._client_id],
            "manufacturer": "BAUER GROUP",
            "model": "Teo der Topf",
            "name": "Mein IoT Pflanztopf",
        }

        # Standard sensors
        standard_sensors = {
            "temperature": "°C",
            "atmospheric_pressure": "hPa",
            "illuminance": "lux"
        }
        for sensor, unit in standard_sensors.items():
            payload = {
                "device": device_info,
                "name": f"{sensor} ({self._client_id})",
                "state_topic": f"{self._base_topic}/sensor/{self._client_id}/{sensor}/state",
                "device_class": f"{sensor}",
                "unit_of_measurement": unit,
                "unique_id": f"{self._client_id}_{sensor}",
            }
            self._publish_mqtt(f"{self._base_topic}/sensor/{self._client_id}/{sensor}/config", json.dumps(payload), retain=True)
            self._log.debug(f"HomeAssistant - Registering sensor '{sensor}' ({unit}).")

        # ADS1115 sensors
        for i in range(4):
            sensor_name = "moisture" if i == 0 else f"ad-channel{i}"
            payload = {
                "device": device_info,
                "name": f"{sensor_name} ({self._client_id})",
                "state_topic": f"{self._base_topic}/sensor/{self._client_id}/{sensor_name}/state",
                "unit_of_measurement": "%" if sensor_name == "moisture" else "ADC",
                "unique_id": f"{self._client_id}_{sensor_name}",
            }
            self._publish_mqtt(f"{self._base_topic}/sensor/{self._client_id}/{sensor_name}/config", json.dumps(payload), retain=True)
            self._log.debug(f"HomeAssistant - Registering sensor '{sensor_name}'.")

    def _publish_mqtt(self, topic, payload, retain=False):
        try:
            self._client.publish(topic, payload, retain=retain)
            #self._log.debug(f"HomeAssistant - MQTT message sent to '{topic}'. Payload: {payload}")
        except Exception as e:
            self._log.warning(f"HomeAssistant - Failed to publish message: {str(e)}")

    def __sensor_manager_callback(self, sensor_manager: SensorManager):
        payload = json.dumps(sensor_manager.temperature)
        self._publish_mqtt(f"{self._base_topic}/sensor/{self._client_id}/temperature/state", payload)

        payload = json.dumps(sensor_manager.pressure)
        self._publish_mqtt(f"{self._base_topic}/sensor/{self._client_id}/atmospheric_pressure/state", payload)

        payload = json.dumps(sensor_manager.light_intensity)
        self._publish_mqtt(f"{self._base_topic}/sensor/{self._client_id}/illuminance/state", payload)

        # Convert the ADC values to percentages and build the payloads
        for i, value in enumerate(sensor_manager.ads1x15_channel_values):
            sensor_name = "moisture" if i == 0 else f"ad-channel{i}"
            if sensor_name == "moisture":
                value = round(self._conversion_soil_moisture(value), 2)  # Only convert soil moisture values to percentages
            payload = json.dumps(value)  # Send the value directly

            # Publish the sensor values
            self._publish_mqtt(f"{self._base_topic}/sensor/{self._client_id}/{sensor_name}/state", payload)

    @staticmethod
    def _conversion_to_relative(ad_value):
        return (ad_value / 32767) * 100

    def _conversion_soil_moisture(self, ad_value):
        soil_range = self._config.SOIL_MAX - self._config.SOIL_MIN
        relative_ad = max(min(ad_value, self._config.SOIL_MAX), self._config.SOIL_MIN) - self._config.SOIL_MIN
        return 100 - ((relative_ad / soil_range) * 100)

    def stop(self):
        self._log.info("HomeAssistant - Stopping MQTT client...")
        self._client.loop_stop()
        self._client.disconnect()

    def __del__(self):
        if self._client is not None:
            self._log.debug("HomeAssistant - MQTT client is being destroyed. Stopping MQTT client...")
            self.stop()
