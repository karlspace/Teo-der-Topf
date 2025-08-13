# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

#######################################################################################################################
#
# Description :  Package for Toni der Topf
# Author      :  Karl Bauer (karl.bauer@bauer-group.com) / www.bauer-group.com
#
#######################################################################################################################

# System Imports
import threading
import time

# Local Imports
from .configuration import Configuration
from .applogger import ApplicationLogger

from .displaymanager import DisplayManager, Emotions
from .sensormanager import SensorManager
from .homeassistantsensor import HomeAssistantSensor

#######################################################################################################################

class Application:
    def __init__(self, config: Configuration):
        self._log = ApplicationLogger(level=config.LOG_LEVEL)
        self._log.debug("Application Class Initializing...")

        self._config = config

        self._app_thread_is_running = False
        self._app_thread = None

        self.display_manager = DisplayManager(self._log, frame_rate=10, frames_skip=5, assets_folder='assets/emotion', shift_x=-25, rotate=0)
        self.sensor_manager = SensorManager(bmp280_address=0x76, bh1750_address=0x23, ads1x15_address=0x48)
        self.ha_client = None

    def start_application(self):
        if not self._app_thread_is_running:
            self._app_thread_is_running = True

            # Start Display Manager
            self.display_manager.start()

            # Start Application Thread
            self._app_thread = threading.Thread(target=self._app_thread_run)
            self._app_thread.start()

            self._log.debug("Application Started...")

    def stop_application(self):
        self._app_thread_is_running = False

        # Wait for Thread
        if self._app_thread is not None:
            self._app_thread.join()

        # Stop HomeAssistant Client
        if self.ha_client is not None:
            self.ha_client.stop()
            self.ha_client = None

        # Stop sensors
        self.sensor_manager.stop()

        # Stop Display Manager
        self.display_manager.stop()

        self._log.debug("Application Stopped...")

    ###################################################################################################################

    def _app_thread_run(self):
        self._log.debug("Application Logic Running...")

        # Telemetry
        if self._config.HOMEASSISTANT_ENABLED:
            self._log.info(f"Starting Telemetry for HomeAssistant using MQTT Server {self._config.HOMEASSISTANT_MQTT_SERVER}")
            self.ha_client = HomeAssistantSensor(mqtt_server=self._config.HOMEASSISTANT_MQTT_SERVER,
                                                ha_id=self._config.HOMEASSISTANT_ID,
                                                sensor_manager=self.sensor_manager,
                                                app_logger=self._log,
                                                config=self._config,
                                                username=self._config.HOMEASSISTANT_MQTT_USER,
                                                password=self._config.HOMEASSISTANT_MQTT_PASSWORD)

        # Application
        self._log.info("Starting Visualization...")
        while self._app_thread_is_running:
            time.sleep(1)
            self.log_sensor_values()
            self.display_manager.set_emotion( self.apply_emotion_face() )

    ###################################################################################################################

    def log_sensor_values(self):
        temperature_str = f"Temperature: {self.sensor_manager.temperature:.2f} °C" if self.sensor_manager.temperature is not None else "Temperature: -"
        pressure_str = f"Pressure: {self.sensor_manager.pressure:.2f} hPa" if self.sensor_manager.pressure is not None else "Pressure: -"
        light_intensity_str = f"Light Intensity: {self.sensor_manager.light_intensity:.2f} lux" if self.sensor_manager.light_intensity is not None else "Light Intensity: -"

        ads1x15_values_str = ''
        if self.sensor_manager.ads1x15_channel_values is not None:
            ads1x15_values_str = ', '.join(
                f'Ch{i}: {val}' if val is not None else f'Ch{i}: -' for i, val in
                enumerate(self.sensor_manager.ads1x15_channel_values))
        else:
            ads1x15_values_str = "-"

        self._log.info(f"{temperature_str} / {pressure_str} / {light_intensity_str}")
        self._log.info(f"A/D: {ads1x15_values_str}")
        self._log.info(f"Display Emotion: {self.display_manager._current_emotion.value}")

    ###################################################################################################################
    def show_random_emotions(self):
        counter = 0  # Initialize a counter
        emotions = [ Emotions.FREEZE, Emotions.HAPPY, Emotions.HOT, Emotions.SAVORY, Emotions.SLEEPY, Emotions.THIRSTY ]
        while self._app_thread_is_running:
            time.sleep(1)
            if counter % 10 == 0:  # Every 10 seconds
                emotion = emotions[counter // 10 % len(emotions)]  # Cycle through the emotions
                self.display_manager.set_emotion(emotion)  # Switch emotion
            counter += 1  # Increase the counter each second

    ###################################################################################################################
    def apply_emotion_face(self):
        # Light
        if self.sensor_manager.light_intensity is not None and \
                self.sensor_manager.light_intensity < self._config.NIGHT_MODE_BELOW:
            return Emotions.SLEEPY

        # Temperature
        elif self.sensor_manager.temperature is not None and \
                self.sensor_manager.temperature < self._config.TEMPERATURE_COLD_BELOW:
            return Emotions.FREEZE
        elif self.sensor_manager.temperature is not None and \
                self.sensor_manager.temperature > self._config.TEMPERATURE_HOT_ABOVE:
            return Emotions.HOT

        # Soil
        elif self.sensor_manager.ads1x15_channel_values[0] is not None and \
                self.sensor_manager.ads1x15_channel_values[0] > self._config.SOIL_DRY_ABOVE:
            return Emotions.THIRSTY
        elif self.sensor_manager.ads1x15_channel_values[0] is not None and \
                self.sensor_manager.ads1x15_channel_values[0] < self._config.SOIL_WET_BELOW:
            return Emotions.SAVORY

        # Default
        return Emotions.HAPPY

#######################################################################################################################
