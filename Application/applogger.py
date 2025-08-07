# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

#######################################################################################################################
#
# Description :  Package for Toni der Topf
# Author      :  Karl Bauer (karl.bauer@bauer-group.com) / www.bauer-group.com
#
#######################################################################################################################

# System Imports
import sys
import logging
from logging import Logger, StreamHandler
import colorlog

#######################################################################################################################

class ApplicationLogger(Logger):
    def __init__(self, name = "ApplicationLogger", level = logging.DEBUG):
        super().__init__(name, level)

        # Set up logging
        # Create a colorized formatter
        formatter = colorlog.ColoredFormatter(

            '%(log_color)s%(asctime)s: %(levelname)s - %(message)s',
            log_colors={
                'DEBUG': 'white',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
        )

        # Create a console handler with the colorized formatter
        console_handler = StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        # Add the console handler to the logger
        self.addHandler(console_handler)

#######################################################################################################################
