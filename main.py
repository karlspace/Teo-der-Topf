#!/usr/bin/python

# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

#######################################################################################################################
#
# Description :  Toni der Topf
# Author      :  Karl Bauer (karl.bauer@bauer-group.com) / www.bauer-group.com
#
#######################################################################################################################

# Version
from version import __version__

# System Imports
import sys
import os
import signal
import time
import logging

# Local Imports
from Application.configuration import Configuration
from Application.app import Application

#######################################################################################################################

class AppMain:
    def __init__(self):
        self.is_running = False
        self._initialize()

    def _initialize(self):
        self.Configuration = Configuration()
        self.Application = Application(config=self.Configuration)

        signal.signal(signal.SIGTERM, self._stop_signal)

    def _stop_signal(self, signal_received, frame):
        print('SIGTERM Signal! => Shutting Down...')
        self.is_running = False

    def run(self):
        print("--- Application Start ---", end=os.linesep)
        print(f"Application Version: {__version__}")

        self.Configuration.show_configuration()

        print("Cancel with CTRL+C", end=os.linesep)

        # Start Application
        self.Application.start_application()
        self.is_running = True

        # Sleep Main Thread
        try:
            while self.is_running:
                #sys.stdout.write('.')
                #sys.stdout.flush()
                time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting Down (CTRL+C) ...")
            self.is_running = False

        # Stop Application
        self.Application.stop_application()

        print(f"", end=os.linesep)
        print("--- Application Stop ---", end=os.linesep)

#######################################################################################################################
### Main Programm Code ###
if __name__ == "__main__":
    try:
        app = AppMain()
        app.run()
    except KeyboardInterrupt:
        pass

#######################################################################################################################
