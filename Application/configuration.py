# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

#######################################################################################################################
#
# Description :  Package for Toni der Topf
# Author      :  Karl Bauer (karl.bauer@bauer-group.com) / www.bauer-group.com
#
#######################################################################################################################

# System Imports
import os
from dotenv import load_dotenv
from pathlib import Path
import logging

# Local Imports
from .applogger import ApplicationLogger

#######################################################################################################################

class Configuration:
    def __init__(self):
        self._log = None
        self._initialize()

    def _initialize(self):
        config_from_environment = os.environ.get('CONFIG_FROM_ENVIRONMENT', 'false').lower() == 'true'
        if not config_from_environment:
            # Load Local .env File to Environment
            env_path = Path.cwd() / '.env'
            load_dotenv(dotenv_path=env_path)

        # Set Variables
        self.LOG_LEVEL = Configuration.loglevel_from_string(os.environ.get('LOG_LEVEL', "DEBUG"))

        self.SOIL_MAX = int(os.environ.get('SOIL_MAX', 18600))
        self.SOIL_MIN = int(os.environ.get('SOIL_MIN', 6900))
        self.SOIL_DRY_ABOVE = int(os.environ.get('SOIL_DRY_ABOVE', 14500))
        self.SOIL_WET_BELOW = int(os.environ.get('SOIL_WET_BELOW', 9500))

        self.TEMPERATURE_COLD_BELOW = float(os.environ.get('TEMPERATURE_COLD_BELOW', 18.0))
        self.TEMPERATURE_HOT_ABOVE = float(os.environ.get('TEMPERATURE_HOT_ABOVE', 24.0))

        self.NIGHT_MODE_BELOW = float(os.environ.get('NIGHT_MODE_BELOW', 5.00))

        self.HOMEASSISTANT_ENABLED = os.environ.get('HOMEASSISTANT_ENABLED', 'false').lower() == 'true'
        self.HOMEASSISTANT_ID = os.environ.get('HOMEASSISTANT_ID', 'TeoTopf')
        self.HOMEASSISTANT_MQTT_SERVER = os.environ.get('HOMEASSISTANT_MQTT_SERVER', 'undefined')
        self.HOMEASSISTANT_MQTT_USER = os.environ.get('HOMEASSISTANT_MQTT_USER', 'undefined')
        self.HOMEASSISTANT_MQTT_PASSWORD = os.environ.get('HOMEASSISTANT_MQTT_PASSWORD', 'undefined')

        # Logger Instance
        self._log = ApplicationLogger(level=self.LOG_LEVEL)

    def show_configuration(self):
        self._log.info("Configuration:")
        self._log.info(f"|- Soil Sensor - DRY: > {self.SOIL_DRY_ABOVE}")
        self._log.info(f"|- Soil Sensor - WET: < {self.SOIL_WET_BELOW}")

        self._log.info(f"|- Temperature - HOT: > {self.TEMPERATURE_HOT_ABOVE}")
        self._log.info(f"|- Temperature - COLD: < {self.TEMPERATURE_COLD_BELOW}")

        self._log.info(f"|- Night Mode: < {self.NIGHT_MODE_BELOW}")

        self._log.info(f"|- HomeAssistant Enabled: {self.HOMEASSISTANT_ENABLED}")
        self._log.info(f"|- HomeAssistant MQTT Server: {self.HOMEASSISTANT_MQTT_SERVER}")

        self._log.info(f"|- Logging Level: {os.environ.get('LOG_LEVEL', 'DEBUG')} ({self.LOG_LEVEL})")
        self._log.info("--------------------------------------")

    ###################################################################################################################

    @staticmethod
    def loglevel_from_string(log_level: str):
        return logging.getLevelName(log_level)

#######################################################################################################################
