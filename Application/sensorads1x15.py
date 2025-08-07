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
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class SensorADS1x15:
    def __init__(self, i2c_bus = busio.I2C(board.SCL, board.SDA), address=0x48, change_threshold=50, polling_rate=1, gain=1.0):
        self.ads = ADS.ADS1115(i2c=i2c_bus, address=address, gain=gain)
        self.change_threshold = change_threshold
        self.polling_rate = polling_rate

        # Set up initial readings
        self.channels = [AnalogIn(self.ads, ADS.P0),
                         AnalogIn(self.ads, ADS.P1),
                         AnalogIn(self.ads, ADS.P2),
                         AnalogIn(self.ads, ADS.P3)]
        self.last_values = [channel.value for channel in self.channels]

        # Set up list for callback functions
        self.callbacks = []

        self.polling_thread = threading.Thread(target=self._poll_sensor)
        self.polling_thread.daemon = True
        self.polling_thread.start()

    def register_callback(self, callback):
        self.callbacks.append(callback)

        # Immediately call the new callback with the current sensor values
        current_values = [channel.value for channel in self.channels]
        for i, value in enumerate(current_values):
            callback(i, value)  # Pass channel number and current value to callback

    def read(self):
        # Get current readings
        current_values = [channel.value for channel in self.channels]

        return current_values

    def _poll_sensor(self):
        while True:
            # Get current readings
            current_values = [channel.value for channel in self.channels]

            # If any reading has changed significantly, call all callback functions
            for i in range(4):
                if abs(current_values[i] - self.last_values[i]) > self.change_threshold:
                    for callback in self.callbacks:
                        callback(i, current_values[i])  # Pass channel number and new value to callback

            # Save current readings for next comparison
            self.last_values = current_values

            # Wait for the next poll
            time.sleep(self.polling_rate)
