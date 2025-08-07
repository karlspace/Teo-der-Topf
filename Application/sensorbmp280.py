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
import board
import busio
import adafruit_bmp280

class SensorBMP280:
    def __init__(self, i2c_bus = busio.I2C(board.SCL, board.SDA), address=0x76, change_threshold=0.1, polling_rate=1):
        self.bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c_bus, address)
        self.change_threshold = change_threshold
        self.polling_rate = polling_rate

        # Set up initial readings
        self.last_temperature = round(self.bmp280.temperature, 2)
        self.last_pressure = round(self.bmp280.pressure, 2)

        # Set up list for callback functions
        self.callbacks = []

        self.polling_thread = threading.Thread(target=self._poll_sensor)
        self.polling_thread.daemon = True
        self.polling_thread.start()

    def register_callback(self, callback):
        self.callbacks.append(callback)

        # Immediately call the new callback with the current sensor values
        current_temperature = round(self.bmp280.temperature, 2)
        current_pressure = round(self.bmp280.pressure, 2)
        callback(current_temperature, current_pressure)

    def read(self):
        # Get current readings
        current_temperature = round(self.bmp280.temperature, 2)
        current_pressure = round(self.bmp280.pressure, 2)

        return current_temperature, current_pressure

    def _poll_sensor(self):
        while True:
            # Get current readings
            current_temperature = round(self.bmp280.temperature, 2)
            current_pressure = round(self.bmp280.pressure, 2)

            # If readings have changed significantly, call all callback functions
            if abs(current_temperature - self.last_temperature) > self.change_threshold or \
               abs(current_pressure - self.last_pressure) > self.change_threshold:
                for callback in self.callbacks:
                    callback(current_temperature, current_pressure)

            # Save current readings for next comparison
            self.last_temperature = current_temperature
            self.last_pressure = current_pressure

            # Wait for the next poll
            time.sleep(self.polling_rate)
