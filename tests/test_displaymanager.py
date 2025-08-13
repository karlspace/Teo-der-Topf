import sys
import types
from pathlib import Path

from PIL import Image


# Stub hardware-specific modules before importing DisplayManager
digitalio = types.ModuleType("digitalio")


class DummyDIO:
    def __init__(self, pin):
        self.value = False

    def switch_to_output(self):
        pass


digitalio.DigitalInOut = DummyDIO

board = types.ModuleType("board")
board.CE0 = board.D25 = board.D24 = board.D23 = board.SCL = board.SDA = None
board.SPI = lambda: None

adafruit_rgb_display = types.ModuleType("adafruit_rgb_display")
ili9341_module = types.ModuleType("ili9341")


class DummyDisplay:
    def __init__(self, *args, **kwargs):
        pass

    def image(self, img):
        pass


ili9341_module.ILI9341 = DummyDisplay
adafruit_rgb_display.ili9341 = ili9341_module

sys.modules["digitalio"] = digitalio
sys.modules["board"] = board
sys.modules["adafruit_rgb_display"] = adafruit_rgb_display
sys.modules["adafruit_rgb_display.ili9341"] = ili9341_module

root_path = Path(__file__).resolve().parents[1]
sys.path.append(str(root_path))

from Application.displaymanager import DisplayManager


def test_shift_and_wrap_right():
    img = Image.new("RGB", (3, 1))
    img.putdata([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
    shifted = DisplayManager._shift_and_wrap(img, 1)
    assert list(shifted.getdata()) == [
        (0, 0, 255),
        (255, 0, 0),
        (0, 255, 0),
    ]


def test_shift_and_wrap_left():
    img = Image.new("RGB", (3, 1))
    img.putdata([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
    shifted = DisplayManager._shift_and_wrap(img, -1)
    assert list(shifted.getdata()) == [
        (0, 255, 0),
        (0, 0, 255),
        (255, 0, 0),
    ]

