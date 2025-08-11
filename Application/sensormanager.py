# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

#######################################################################################################################
#
# Description :  Package for Toni der Topf
# Author      :  Karl Bauer (karl.bauer@bauer-group.com) / www.bauer-group.com
#
#######################################################################################################################

# System Imports
import board
import busio

# Local Imports
from .sensorads1x15 import SensorADS1x15
from .sensorbh1750 import SensorBH1750
from .sensorbmp280 import SensorBMP280

class SensorManager:
    def __init__(self, i2c_bus=None, bmp280_address=0x76, bh1750_address=0x23, ads1x15_address=0x48):
        # Create a single I2C bus instance
        if i2c_bus is None:
            i2c_bus = busio.I2C(board.SCL, board.SDA)
        self._i2c_bus = i2c_bus

        # Initialize list for manager-specific callbacks
        self.callbacks = []

        # Initialize sensor data storage
        self.bmp280_data = (None, None)  # Temperature, pressure
        self.bh1750_data = None  # Light intensity
        self.ads1x15_data = [None] * 4  # Channel readings

        # Create sensor objects
        self._sensor_bmp280 = SensorBMP280(i2c_bus=self._i2c_bus, address=bmp280_address)
        self._sensor_bh1750 = SensorBH1750(i2c_bus=self._i2c_bus, address=bh1750_address)
        self._sensor_ads1x15 = SensorADS1x15(i2c_bus=self._i2c_bus, address=ads1x15_address)

        # Register this SensorManager as a callback
        self._sensor_bmp280.register_callback(self._bmp280_callback)
        self._sensor_bh1750.register_callback(self._bh1750_callback)
        self._sensor_ads1x15.register_callback(self._ads1x15_callback)

    # Callbacks to handle sensor data updates
    def notify_callbacks(self):
        for callback in self.callbacks:
            callback(self)

    def _bmp280_callback(self, temperature, pressure):
        self.bmp280_data = (temperature, pressure)
        self.notify_callbacks()

    def _bh1750_callback(self, light_intensity):
        self.bh1750_data = light_intensity
        self.notify_callbacks()

    def _ads1x15_callback(self, channel, value):
        self.ads1x15_data[channel] = value
        self.notify_callbacks()

    # Properties to expose sensor data
    @property
    def temperature(self):
        (temperature, pressure) = self.bmp280_data
        return temperature

    @property
    def pressure(self):
        (temperature, pressure) = self.bmp280_data
        return pressure

    @property
    def light_intensity(self):
        return self.bh1750_data

    @property
    def ads1x15_channel_values(self):
        return self.ads1x15_data

    def register_callback(self, callback):
        # Register a callback to receive updates from this SensorManager.
        # The callback should be a function that takes a single argument: the SensorManager instance.
        self.callbacks.append(callback)

        # Immediately call the new callback with the current sensor values
        callback(self)
