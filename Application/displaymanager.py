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
import time
import threading
from PIL import Image, ImageDraw
import shutil
import json
import digitalio
import board
from adafruit_rgb_display import ili9341

# Local Imports
from .applogger import ApplicationLogger


class Emotions:
    FREEZE = "freeze"
    HAPPY = "happy"
    HOT = "hot"
    SAVORY = "savory"
    SLEEPY = "sleepy"
    THIRSTY = "thirsty"


class DisplayManager(threading.Thread):
    _BAUDRATE = 80000000

    _DISP_WIDTH = 320
    _DISP_HEIGHT = 240

    _VALID_EMOTIONS = [
        Emotions.FREEZE,
        Emotions.HAPPY,
        Emotions.HOT,
        Emotions.SAVORY,
        Emotions.SLEEPY,
        Emotions.THIRSTY,
    ]

    def __init__(
        self,
        app_logger: ApplicationLogger,
        frame_rate=5,
        frames_skip=0,
        default_emotion=Emotions.HAPPY,
        assets_folder="assets/emotion",
        shift_x=0,
        rotate=0,
    ):
        threading.Thread.__init__(self)
        self._log = app_logger
        self._log.debug("Initializing Display Manager...")

        self._frame_rate = frame_rate
        self._frames_skip = max(1, frames_skip)
        self._current_emotion = default_emotion
        self._assets_folder = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), assets_folder
        )
        self._shift_x = shift_x
        self._rotate = rotate
        self._is_running = False
        self._temp_folder = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "assets/temp"
        )

        # Backlight setup
        self._backlight = digitalio.DigitalInOut(board.D23)
        self._backlight.switch_to_output()

        # Display a Pattern after Setup
        self._setup_display()
        self._display_pattern()
        self._backlight.value = True

        # Prepare the Images
        self._prepare_images()

    def _prepare_images(self):
        self._log.debug("Checking and preparing images temp folder...")
        settings_path = os.path.join(self._temp_folder, "displaysettings.json")
        if os.path.exists(settings_path):
            with open(settings_path, "r") as f:
                settings = json.load(f)
                previous_rotate = settings.get("rotate", None)
                previous_shift_x = settings.get("shift_x", None)
        else:
            previous_rotate = None
            previous_shift_x = None

        if self._shift_x != previous_shift_x or self._rotate != previous_rotate:
            self._log.debug(
                "Shift/rotate value changed or not found. Regenerating images..."
            )

            # Clean up and generate new images
            if os.path.exists(self._temp_folder):
                shutil.rmtree(self._temp_folder)
            os.makedirs(self._temp_folder, exist_ok=True)

            self._generate_temporary_images()

            # Store new settings
            with open(settings_path, "w") as f:
                json.dump({"rotate": self._rotate, "shift_x": self._shift_x}, f)
        else:
            self._log.debug(
                "No change in shift/rotate value detected. Reusing existing images."
            )

    def _generate_temporary_images(self):
        self._log.debug("Generating temporary images...")
        # Pre-process all images
        for emotion in self._VALID_EMOTIONS:
            self._log.debug(f"Processing images for emotion {emotion}")
            image_folder_path = os.path.join(self._assets_folder, emotion)
            temp_folder_path = os.path.join(self._temp_folder, emotion)
            os.makedirs(temp_folder_path, exist_ok=True)

            image_files = sorted(
                [f for f in os.listdir(image_folder_path) if f.endswith(".png")]
            )

            for image_file in image_files:
                self._log.debug(f"Processing image {image_file} for emotion {emotion}")
                temp_image_path = os.path.join(temp_folder_path, image_file)
                image_path = os.path.join(image_folder_path, image_file)

                with Image.open(image_path) as image:
                    processed_image = image

                    # Rotate the image
                    if self._rotate != 0:
                        processed_image = processed_image.rotate(self._rotate)

                    # Shift the image
                    if self._shift_x != 0:
                        processed_image = self._shift_and_wrap(
                            processed_image, self._shift_x
                        )

                    processed_image.save(temp_image_path)

    def _setup_display(self):
        # Configuration for CS and DC pins (these are PiTFT defaults):
        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = digitalio.DigitalInOut(board.D24)

        # Setup SPI bus using hardware SPI:
        spi = board.SPI()

        self.disp = ili9341.ILI9341(
            spi,
            rotation=90,
            cs=cs_pin,
            dc=dc_pin,
            rst=reset_pin,
            baudrate=self._BAUDRATE,
        )

    def set_emotion(self, emotion):
        if emotion in self._VALID_EMOTIONS:
            self._current_emotion = emotion
        else:
            raise ValueError(
                f"Invalid emotion: {emotion}. Valid emotions are: {self._VALID_EMOTIONS}"
            )

    @property
    def current_emotion(self):
        """Return the emotion currently being displayed."""
        return self._current_emotion

    def run(self):
        self._is_running = True
        self._backlight.value = True  # Turn on the backlight when starting
        frame_delay = 1.0 / self._frame_rate

        last_emotion = None
        images = []
        frame_counter = 0

        while self._is_running:
            if last_emotion != self._current_emotion:
                # Load the names of all pre-processed PNG images in the temp folder.
                image_folder_path = os.path.join(
                    self._temp_folder, self._current_emotion
                )
                image_files = sorted(
                    [f for f in os.listdir(image_folder_path) if f.endswith(".png")]
                )
                # Load all images into memory.
                images = [
                    Image.open(os.path.join(image_folder_path, image_file))
                    for image_file in image_files
                ]
                last_emotion = self._current_emotion

            for image in images:
                # If emotion changed, break the image loop and restart with new emotion
                if last_emotion != self._current_emotion:
                    break

                if frame_counter % self._frames_skip == 0:
                    self.disp.image(image)

                    # Wait for the next frame.
                    time.sleep(frame_delay)

                frame_counter += 1

                # Check if the thread should stop after processing each image.
                if not self._is_running:
                    return

    def stop(self):
        self._is_running = False
        if self.is_alive():
            # Show a pattern before stopping.
            self._display_pattern()
            self.join()
        self._backlight.value = False  # Turn off the backlight when stopping

    def _display_pattern(self):
        # Create a new image with RGB mode
        image = Image.new("RGB", (self._DISP_WIDTH, self._DISP_HEIGHT))

        # Get a drawing context
        draw = ImageDraw.Draw(image)

        # Draw three stripes
        draw.rectangle([(0, 0), (self._DISP_WIDTH // 3, self._DISP_HEIGHT)], fill="red")
        draw.rectangle(
            [
                (self._DISP_WIDTH // 3, 0),
                (2 * self._DISP_WIDTH // 3, self._DISP_HEIGHT),
            ],
            fill="green",
        )
        draw.rectangle(
            [(2 * self._DISP_WIDTH // 3, 0), (self._DISP_WIDTH, self._DISP_HEIGHT)],
            fill="blue",
        )

        # Display the pattern
        self.disp.image(image)

    @staticmethod
    def _shift_and_wrap(image, x):
        data = image.load()
        new_data = {}

        for y in range(image.size[1]):
            for x_new in range(image.size[0]):
                new_data[(x_new, y)] = data[((x_new - x) % image.size[0], y)]

        new_image = Image.new(image.mode, image.size)
        new_image.putdata(
            [
                new_data[(x, y)]
                for y in range(image.size[1])
                for x in range(image.size[0])
            ]
        )

        return new_image
