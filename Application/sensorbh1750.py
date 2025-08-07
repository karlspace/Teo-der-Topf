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
import adafruit_bh1750

class SensorBH1750:
    def __init__(self, i2c_bus = busio.I2C(board.SCL, board.SDA), address=0x23, change_threshold=1.0, polling_rate=1):
        self.bh1750 = adafruit_bh1750.BH1750(i2c_bus, address)
        self.change_threshold = change_threshold
        self.polling_rate = polling_rate

        # Set up initial reading
        self.last_light_intensity = round(self.bh1750.lux, 2)

        # Set up list for callback functions
        self.callbacks = []

        self.polling_thread = threading.Thread(target=self._poll_sensor)
        self.polling_thread.daemon = True
        self.polling_thread.start()

    def register_callback(self, callback):
        self.callbacks.append(callback)

        # Immediately call the new callback with the current sensor values
        current_light_intensity = round(self.bh1750.lux, 2)
        callback(current_light_intensity)

    def read(self):
        # Get current reading
        current_light_intensity = round(self.bh1750.lux, 2)

        return current_light_intensity

    def _poll_sensor(self):
        while True:
            # Get current reading
            current_light_intensity = round(self.bh1750.lux, 2)

            # If readings have changed significantly, call all callback functions
            if abs(current_light_intensity - self.last_light_intensity) > self.change_threshold:
                for callback in self.callbacks:
                    callback(current_light_intensity)

            # Save current reading for next comparison
            self.last_light_intensity = current_light_intensity

            # Wait for the next poll
            time.sleep(self.polling_rate)

